import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { Store } from '@ngrx/store';
import { CredentialsState } from '@app/features/identity/store/identity.models';
import { selectCredentials } from '@app/features/identity/store/identity.selectors';

@Component({
  selector: 'qr-home-page',
  templateUrl: 'home-page.component.html',
  styleUrls: ['home-page.component.scss'],
})
export class QrHomePageComponent implements OnInit {
  constructor(private router: Router, private store: Store) {}

  ngOnInit() {
    this.store
      .select(selectCredentials)
      .subscribe((credentials: CredentialsState) => {
        if (!credentials) {
          this.router.navigate(['/identity/login']);
        } else {
          this.router.navigate(['/storm']);
        }
      });
  }

  OnSignUp() {
    this.router.navigate(['/identity/sign-up']);
  }
}
