// angular
import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core';
import {
  FormBuilder,
  FormControl,
  FormGroup,
  Validators,
} from '@angular/forms';

// validator
import { CreditCardValidators } from 'angular-cc-library';

// models
import { PaymentInformation } from '../../models/Payment.models';

@Component({
  selector: 'qr-payment-form-credit-card',
  templateUrl: './payment-form-credit-card.component.html',
  styleUrls: ['./payment-form-credit-card.component.scss'],
})
export class QrPaymentFormCardComponent implements OnInit {
  paymentForm!: FormGroup;

  @Input() amount: number;
  @Input() subscriptionPlanId: number;
  @Output() submitPayment = new EventEmitter();

  constructor(private fb: FormBuilder) {}

  ngOnInit() {
    this.paymentForm = this.fb.group({
      firstName: [null, [Validators.required]],
      lastName: [null, [Validators.required]],
      cardNumber: [null, [CreditCardValidators.validateCCNumber]],
      expirationDate: [null, [CreditCardValidators.validateExpDate]],
      cvc: [
        null,
        [Validators.required, Validators.minLength(3), Validators.maxLength(4)],
      ],
      billingAddress: [null, [Validators.required]],
      city: [null, [Validators.required]],
      state: [null, [Validators.required]],
      zipPostalCode: [
        null,
        [
          Validators.required,
          Validators.minLength(5),
          Validators.pattern('^[0-9]*$'),
        ],
      ],
    });
  }

  submitForm(): void {
    console.log(this.paymentForm.controls);
    for (const i in this.paymentForm.controls) {
      this.paymentForm.controls[i].markAsDirty();
      this.paymentForm.controls[i].updateValueAndValidity();
    }
    if (this.paymentForm.status === 'VALID') {
      const paymentInformation: PaymentInformation = {
        firstName: this.paymentForm.get('firstName').value,
        lastName: this.paymentForm.get('lastName').value,
        cardNumber: this.paymentForm.get('cardNumber').value,
        expirationDate: this.paymentForm.get('expirationDate').value,
        cvc: this.paymentForm.get('cvc').value,
        billingAddress: this.paymentForm.get('billingAddress').value,
        city: this.paymentForm.get('city').value,
        state: this.paymentForm.get('state').value,
        zipCode: this.paymentForm.get('zipPostalCode').value,
        amount: this.amount,
        subscriptionPlanId: this.subscriptionPlanId,
      };
      paymentInformation.cardNumber = paymentInformation.cardNumber.replace(
        /\s/g,
        ''
      );
      paymentInformation.expirationDate = paymentInformation.expirationDate.replace(
        /\s/g,
        ''
      );
      this.submitPayment.emit(paymentInformation);
    }
  }
}
