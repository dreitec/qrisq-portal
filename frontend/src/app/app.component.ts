// angular
import { Component, OnDestroy, OnInit } from '@angular/core';
import { createSelector, Store } from '@ngrx/store';
import { iif, Observable, of, Subscription } from 'rxjs';
import { catchError, take } from 'rxjs/operators';
import { QrIdentityService } from './features/identity/services/identity.service';
import {
  actionAccessTokenRefreshed,
  actionSignOut,
} from './features/identity/store/identity.actions';
import {
  CredentialsState,
  SignedUserState,
} from './features/identity/store/identity.models';
import {
  selectCredentials,
  selectSignedUser,
} from './features/identity/store/identity.selectors';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss'],
})
export class AppComponent implements OnInit {
  title = 'Qrisq';
  credentials: CredentialsState;
  isUserLogin: boolean;
  userFirstName: string;
  isAdmin: boolean;

  constructor(
    private store: Store,
    private identityService: QrIdentityService
  ) {}

  ngOnInit(): void {
    this.store
      .select(selectSignedUser)
      .subscribe((signedUser: SignedUserState) => {
        if (signedUser) {
          this.isUserLogin = true;
          this.userFirstName = signedUser.user.firstName;
          this.isAdmin = signedUser.user.isAdmin;
        } else {
          this.isUserLogin = false;
          this.userFirstName = '';
          this.isAdmin = false;
        }
      });

    this.store
      .select(selectCredentials)
      .subscribe((credentials: CredentialsState) => {
        if (credentials) {
          this.credentials = credentials;
        }

        // validating credentials
        // this.identityService
        //   .validateAccessToken(credentials.accessToken)
        //   .subscribe((isAccessTokenValid) => {
        //     if (isAccessTokenValid) {
        //       console.log('accessToken valid');
        //       this.store
        //         .select(selectSignedUser)
        //         .subscribe((signedUser: SignedUserState) => {
        //           this.isUserLogin = true;
        //           this.userFirstName = signedUser.user.firstName;
        //         });
        //     } else {
        //       console.log('accessToken not valid');
        //       this.identityService
        //         .refreshCredentials(credentials.refreshToken)
        //         .pipe(
        //           take(1),
        //           catchError((error) => {
        //             this.store.dispatch(
        //               actionSignOut({ refreshToken: credentials.refreshToken })
        //             );
        //             this.isUserLogin = false;
        //             this.userFirstName = '';
        //             return of(error);
        //           })
        //         )
        //         .subscribe((response) => {
        //           console.log(response);
        //           if (response) {
        //             this.store.dispatch(
        //               actionAccessTokenRefreshed({
        //                 newAccessToken: response.access,
        //               })
        //             );
        //             this.store
        //               .select(selectSignedUser)
        //               .subscribe((signedUser: SignedUserState) => {
        //                 this.isUserLogin = true;
        //                 this.userFirstName = signedUser.user.firstName;
        //               });
        //           }
        //         });
        //     }
        //   });
      });
  }

  onLogout($event) {
    const refreshToken = this.credentials.refreshToken;
    this.store.dispatch(actionSignOut({ refreshToken }));
  }
}
