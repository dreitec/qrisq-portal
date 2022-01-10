import { Component, OnInit } from '@angular/core';
import {ActivatedRoute, Router} from '@angular/router';
import {Store} from '@ngrx/store';
import {actionVerifyPayment} from '@identity/store/identity.actions';
import {selectSignedUser} from '@identity/store/identity.selectors';
import {take} from 'rxjs/operators';
import {SignedUserState} from '@identity/store/identity.models';

@Component({
  selector: 'qr-payment-successful-page',
  templateUrl: './payment-successful.component.html',
  styleUrls: ['./payment-successful.component.scss'],
})
export class QrPaymentSuccessfulPageComponent implements OnInit {
  loading = true;
  loadingMessage = 'Verifying your payment. This may take a few moments.';
  signedUser: SignedUserState;

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private store: Store
  ) {}

  ngOnInit() {
    this.store.dispatch(actionVerifyPayment());
    this.store
      .select(selectSignedUser)
      .pipe(take(1))
      .subscribe((signedUser) => {
          this.signedUser = signedUser;
          this.loading = !this.signedUser.user.hasPaid;
      });
  }

  onRegisterSubmit() {
    this.router.navigate(['storm']);
  }
}
