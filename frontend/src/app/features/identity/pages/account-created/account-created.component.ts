import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'qr-account-created',
  templateUrl: './account-created.component.html',
  styleUrls: ['./account-created.component.scss'],
})
export class QrAccountCreatedPageComponent implements OnInit {
  constructor(private router: Router) {}

  ngOnInit() {}

  toStorm() {
    this.router.navigate(['storm']);
  }
}
