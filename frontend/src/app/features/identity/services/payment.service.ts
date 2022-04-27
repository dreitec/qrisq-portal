import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { environment } from '@env';
import {
  PaymentInformation,
  PaypalPaymentInformation, VerifySubscriptionPaymentRequest,
} from '../models/Payment.models';

@Injectable({
  providedIn: 'root',
})
export class QrPaymentService {
  constructor(private httpClient: HttpClient) {}

  processPayment(paymentInformation: PaymentInformation) {
    return this.httpClient.post(
      environment.API_URL + '/create-subscription',
      {
        token: paymentInformation.token,
        amount: paymentInformation.amount,
        subscription_plan_id: paymentInformation.subscriptionPlanId,
        payment_gateway: 'fluidpay'
      },
      {
        headers: { 'Content-type': 'application/json; charset=utf-8' },
      }
    );
  }

  createSubscriptionFromPaypal(paymentInformation: PaypalPaymentInformation) {
    return this.httpClient.post(
      environment.API_URL + '/create-subscription',
      {
        subscription_plan_id: paymentInformation.subscriptionPlanId,
        payment_gateway: 'paypal'
      },
      {
        headers: { 'Content-type': 'application/json; charset=utf-8' },
      }
    );
  }

  verifySubscriptionPayment(verifySubscriptionPaymentRequest: VerifySubscriptionPaymentRequest) {
    return this.httpClient.get(
      `${environment.API_URL}/verify-subscription-payment${verifySubscriptionPaymentRequest.paypalSubscriptionId
        ? `?paypal_subscription_id=${encodeURIComponent(verifySubscriptionPaymentRequest.paypalSubscriptionId)}` : ``}`
    );
  }

}
