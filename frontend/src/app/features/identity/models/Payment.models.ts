export interface PaymentInformation {
  firstName: string;
  lastName: string;
  cardNumber: string;
  expirationDate: string;
  cvc: string;
  billingAddress: string;
  city: string;
  state: string;
  zipCode: string;
  amount: number;
  subscriptionPlanId: number;
}

export interface PaypalPaymentInformation {
  payment_id: string;
  payment_gateway: string;
}
