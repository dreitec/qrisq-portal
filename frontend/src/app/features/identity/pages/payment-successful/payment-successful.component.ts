import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'qr-payment-successful-page',
  templateUrl: './payment-successful.component.html',
  styleUrls: ['./payment-successful.component.scss'],
})
export class QrPaymentSuccessfulPageComponent implements OnInit {
  constructor(private router: Router) {}

  ngOnInit() {}

  onRegisterSubmit() {
    this.router.navigate(['storm']);
  }
}
