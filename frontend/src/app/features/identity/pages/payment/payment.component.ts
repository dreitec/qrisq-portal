// angular
import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { take } from 'rxjs/operators';
import {
  PaymentInformation,
  PaypalPaymentInformation,
} from '../../models/Payment.models';
import { Store } from '@ngrx/store';
import { Observable } from 'rxjs';
import { SignedUserState } from '../../store/identity.models';
import {
  actionProcessPaymentRequest,
  actionProcessPaymentRequestSuccess,
  actionProcessPaypalPaymentRequest,
  actionResetPayment,
} from '../../store/identity.actions';
import {
  selectSignedUser,
  selectPayment,
} from '../../store/identity.selectors';

@Component({
  selector: 'qr-register-payment-page',
  templateUrl: './payment.component.html',
  styleUrls: ['./payment.component.scss'],
})
export class QrPaymentPageComponent implements OnInit {
  paymentMethod = 'card';
  paypalPaymentFailed = false;
  loading = false;
  loadingMessage = '';

  signedUser$: Observable<SignedUserState>;
  signedUser: SignedUserState;

  payment$ = this.store.select(selectPayment);

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private store: Store
  ) {}

  ngOnInit(): void {
    this.store.dispatch(actionResetPayment());
    this.store
      .select(selectSignedUser)
      .pipe(take(1))
      .subscribe((signedUser) => (this.signedUser = signedUser));
  }

  onPaymentMethodChange(paymentMethod) {
    this.store.dispatch(actionResetPayment());
    this.paypalPaymentFailed = false;
  }

  onCreditCardPaymentSubmit(paymentInformation: PaymentInformation) {
    this.store.dispatch(actionProcessPaymentRequest({ paymentInformation }));
  }

  onPaypalPaymentSubmit() {
    this.loading = true;
    this.loadingMessage = 'Redirecting you to Paypal...';
    const paypalPaymentInformation = <PaypalPaymentInformation> {
      subscriptionPlanId: this.signedUser.user.subscription.id
    };
    this.store.dispatch(actionProcessPaypalPaymentRequest({ paypalPaymentInformation }));
  }

}
