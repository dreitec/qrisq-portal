// angular
import { Component, OnInit } from '@angular/core';
import {
  FormBuilder,
  FormControl,
  FormGroup,
  Validators,
} from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';

// paypal
import { IPayPalConfig, ICreateOrderRequest } from 'ngx-paypal';

// guid
import { Guid } from 'guid-typescript';
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

  signedUser$: Observable<SignedUserState>;
  signedUser: SignedUserState;

  payment$ = this.store.select(selectPayment);

  public payPalConfig?: IPayPalConfig;

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private store: Store
  ) {}

  ngOnInit(): void {
    this.initConfig();
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
    console.log(paymentInformation);
    this.store.dispatch(actionProcessPaymentRequestSuccess({ paymentInformation }));
  }

  onPaypalPaymentSubmit() {}

  onPaypalPaymentSucceeded(paymentId: string) {
    const paypalPaymentInformation: PaypalPaymentInformation = {
      payment_id: paymentId,
      payment_gateway: 'paypal',
    };
    this.store.dispatch(
      actionProcessPaypalPaymentRequest({ paypalPaymentInformation })
    );
  }

  private initConfig(): void {
    this.payPalConfig = {
      currency: 'USD',
      clientId:
        'Afw9VdV3ysS1ZTNo5Rmh62oNQrN1FF_p7ehf092cTGNUTAdL2gkmTwkhOczIJu-Wy6BZttv5YNfVMBe-',
      createOrderOnClient: (data) =>
        <ICreateOrderRequest>{
          intent: 'CAPTURE',
          purchase_units: [
            {
              amount: {
                currency_code: 'USD',
                value: this.signedUser.user.subscription.price,
                breakdown: {
                  item_total: {
                    currency_code: 'USD',
                    value: `${this.signedUser.user.subscription.price}`,
                  },
                },
              },
              items: [
                {
                  name: 'Qrisq Subscription',
                  quantity: '1',
                  category: 'DIGITAL_GOODS',
                  unit_amount: {
                    currency_code: 'USD',
                    value: `${this.signedUser.user.subscription.price}`,
                  },
                },
              ],
            },
          ],
        },
      advanced: {
        commit: 'true',
        extraQueryParams: [{ name: 'disable-funding', value: 'credit,card' }],
      },
      style: {
        label: 'paypal',
        layout: 'vertical',
      },
      onApprove: (data, actions) => {
        // console.log(
        //   'onApprove - transaction was approved, but not authorized',
        //   data,
        //   actions
        // );
        // actions.order.get().then((details) => {
        //   console.log(
        //     'onApprove - you can get full order details inside onApprove: ',
        //     details
        //   );
        // });
        // this.registerData.paymentId = Guid.create().toString().substring(0, 8);
        // this.router.navigate([
        //   '/register/payment-successful',
        //   this.registerData,
        // ]);
      },
      onClientAuthorization: (data) => {
        // console.log(
        //   'onClientAuthorization - you should probably inform your server about completed transaction at this point',
        //   data
        // );
        this.onPaypalPaymentSucceeded(data.id);
      },
      onCancel: (data, actions) => {
        this.paypalPaymentFailed = true;
      },
      onError: (err) => {
        this.paypalPaymentFailed = true;
      },
      onClick: (data, actions) => {
        // console.log('onClick', data, actions);
      },
    };
  }
}
