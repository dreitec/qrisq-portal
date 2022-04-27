// angular
import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { take } from 'rxjs/operators';
import Tokenizer from 'fluidpay-tokenizer';
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

  example: any;

  ngOnInit(): void {
    this.example = new Tokenizer({
      url: 'https://sandbox.convenupay.com',
      apikey: 'pub_28IpFFyqkBUo05gAQFKFVNquxcD',
      container: document.querySelector('#subscription-payment'),
      submission: (resp) => {
        const { status, token = '' } = resp;
        if (status === 'success' && token) {
          this.store.dispatch(actionProcessPaymentRequest({
            paymentInformation: {
              token,
              amount: 10,
              subscriptionPlanId: 1,
            }
          }));
        }
      },
      settings: {
        payment: {
          calculateFees: true,
          showTitle: true,
          placeholderCreditCard: '0000 0000 0000 0000',
          showExpDate: true,
          showCVV: true,
          ach: {
            sec_code: 'web', // Default web - web, ccd, ppd, tel
            showSecCode: false // Default false - true to show sec code dropdown
          },
          card: {
            strict_mode: false, // Set to true to allow for 19 digit cards
            requireCVV: false // Default false - true to require cvv
          }
        }
      }
    });
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

  onCreditCardPaymentSubmit() {
    this.example.submit();
    // this.store.dispatch(actionProcessPaymentRequest({ paymentInformation }));
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
