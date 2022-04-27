export interface PaymentInformation {
  // firstName: string;
  // lastName: string;
  // cardNumber: string;
  // expirationDate: string;
  // cvc: string;
  // billingAddress: string;
  // city: string;
  // state: string;
  // zipCode: string;
  amount: number;
  subscriptionPlanId: number;
  token: string;
}

export interface PaypalPaymentInformation {
  subscriptionPlanId: number;
}

export interface PaypalCreateSubscriptionResponse {
  approvalUrl: string;
}

export interface VerifySubscriptionPaymentResponse {
  expired: boolean;
}

export interface VerifySubscriptionPaymentRequest {
  paypalSubscriptionId?: string;
}
