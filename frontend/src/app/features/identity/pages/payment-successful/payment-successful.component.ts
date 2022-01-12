import {Component, OnDestroy, OnInit} from '@angular/core';
import {ActivatedRoute, Router} from '@angular/router';
import {Store} from '@ngrx/store';
import {actionVerifyPayment} from '@identity/store/identity.actions';
import {selectSignedUser} from '@identity/store/identity.selectors';
import {SignedUserState} from '@identity/store/identity.models';
import {VerifySubscriptionPaymentRequest} from '@identity/models/Payment.models';

@Component({
  selector: 'qr-payment-successful-page',
  templateUrl: './payment-successful.component.html',
  styleUrls: ['./payment-successful.component.scss'],
})
export class QrPaymentSuccessfulPageComponent implements OnInit, OnDestroy {
  loading = true;
  loadingMessage = 'Verifying your payment. This may take a few moments.';
  signedUser: SignedUserState;
  signedUserSubscription = null;

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private store: Store
  ) {}

  ngOnInit() {
    // Pass optional params if we were redirected here from paypal.  The subscription_id to verify
    // will be in the url parameters.
    const queryString = window.location.search;
    const verifySubscriptionPaymentRequest = <VerifySubscriptionPaymentRequest> {};
    if (queryString) {
      const urlParams = new URLSearchParams(queryString);
      if (urlParams.has('subscription_id')) {
        verifySubscriptionPaymentRequest.paypalSubscriptionId = urlParams.get('subscription_id');
      }
    }

    this.store.dispatch(actionVerifyPayment({ verifySubscriptionPaymentRequest }));
    this.signedUserSubscription = this.store
      .select(selectSignedUser)
      .subscribe((signedUser) => {
          this.signedUser = signedUser;
          this.loading = !this.signedUser.user.hasPaid;
      });
  }

  ngOnDestroy() {
    this.signedUserSubscription.unsubscribe();
  }

  onRegisterSubmit() {
    this.router.navigate(['storm']);
  }
}
