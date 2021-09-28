import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { actionSignOut } from '@app/features/identity/store/identity.actions';
import { selectCredentials } from '@app/features/identity/store/identity.selectors';
import { Store } from '@ngrx/store';
import { switchMap, take, tap } from 'rxjs/operators';

@Component({
  selector: 'qr-home-page',
  templateUrl: 'home-page.component.html',
  styleUrls: ['home-page.component.scss'],
})
export class QrHomePageComponent implements OnInit {
  constructor(private router: Router, private store: Store) {}

  ngOnInit() {}

  OnSignUp() {
    this.router.navigate(['/identity/sign-up']);
  }
}
