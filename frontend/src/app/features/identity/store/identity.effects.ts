import { QrGeolocationService } from './../services/geolocation.service';
import { Injectable } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { Actions, createEffect, ofType } from '@ngrx/effects';
import { EMPTY, of } from 'rxjs';
import {
  catchError,
  finalize,
  map,
  mergeMap,
  switchMap,
  take,
  tap,
  withLatestFrom,
} from 'rxjs/operators';

import {
  actionCheckServiceAreaRequest,
  actionCheckServiceAreaRequestSuccess,
  actionCreateAccountRequest,
  actionCreateAccountRequestFailed,
  actionCreateAccountRequestSuccess,
  actionGeocodeLocationRequest,
  actionGeocodeLocationRequestSuccess,
  actionProcessPaymentRequestFailed,
  actionProcessPaymentRequestSuccess,
  actionProcessPaypalPaymentRequest, actionProcessPaypalPaymentRequestFailed,
  actionRegisterFormSubmit,
  actionRegisterStart,
  actionServiceAreaAvailable,
  actionServiceAreaUnavailable,
  actionSignInFailed,
  actionSignInRequest,
  actionSignInSuccess,
  actionSignOut,
  actionUpdateGeolocationRequest,
  actionUpdateGeolocationRequestFailed,
  actionUpdateGeolocationRequestSuccess,
  actionVerifyEmailRequest,
  actionVerifyEmailRequestFailed,
  actionVerifyEmailRequestSuccess, actionVerifyPayment,
} from './identity.actions';
import { Store } from '@ngrx/store';
import { selectCredentials, selectSignUp } from './identity.selectors';
import { QrIdentityService } from '../services/identity.service';
import { HttpSignInResponse } from '../models/HttpSignInResponse.models';
import { HttpErrorResponse, HttpResponse } from '@angular/common/http';
import { NzNotificationService } from 'ng-zorro-antd/notification';
import { actionProcessPaymentRequest } from './identity.actions';
import { QrPaymentService } from '../services/payment.service';
import {PaypalCreateSubscriptionResponse, VerifySubscriptionPaymentResponse} from "@identity/models/Payment.models";

@Injectable()
export class IdentityEffects {
  /* -------------------------------------------------------------------------- */
  /*                             Check Service Area                             */
  /* -------------------------------------------------------------------------- */

  // request
  effectCheckServiceAreaRequest = createEffect(() =>
    this.actions$.pipe(
      ofType(actionCheckServiceAreaRequest),
      switchMap((action) =>
        this.identityService
          .checkServiceArea(action.lattitude, action.longitude)
          .pipe(
            map((result: { available: boolean; services: Array<string> }) =>
              actionCheckServiceAreaRequestSuccess({
                available: result.available,
                services: result.services,
              })
            ),
            catchError((error) => EMPTY)
          )
      )
    )
  );

  // success
  effectCheckServiceAreaRequestSuccess = createEffect(() =>
    this.actions$.pipe(
      ofType(actionCheckServiceAreaRequestSuccess),
      map((action) => {
        if (action.available) {
          return actionServiceAreaAvailable({
            onlyWind: !action.services.includes('surge'),
          });
        }
        return actionServiceAreaUnavailable();
      })
    )
  );

  /* -------------------------------------------------------------------------- */
  /*                                Service Area                                */
  /* -------------------------------------------------------------------------- */

  // available
  effectServiceAreaAvailable = createEffect(() =>
    this.actions$.pipe(
      ofType(actionServiceAreaAvailable),
      withLatestFrom(this.store.select(selectSignUp)),
      map(([action, signUp]) => {
        this.router.navigate(
          ['identity', 'sign-up', 'service-area-available'],
          {
            queryParams: {
              lattitude: signUp.lattitude,
              longitude: signUp.longitude,
            },
          }
        );
        return actionGeocodeLocationRequest({
          lattitude: signUp.lattitude,
          longitude: signUp.longitude,
        });
      })
    )
  );

  // unavailable
  effectServiceAreaUnvailable = createEffect(
    () =>
      this.actions$.pipe(
        ofType(actionServiceAreaUnavailable),
        tap((action) =>
          this.router.navigate([
            'identity',
            'sign-up',
            'service-area-unavailable',
          ])
        )
      ),
    { dispatch: false }
  );

  /* -------------------------------------------------------------------------- */
  /*                              Geocode Location                              */
  /* -------------------------------------------------------------------------- */

  // request
  effectGeocodeLocationRequest = createEffect(() =>
    this.actions$.pipe(
      ofType(actionGeocodeLocationRequest),
      switchMap((action) =>
        this.identityService
          .geocodeLocation(action.lattitude, action.longitude)
          .pipe(
            take(1),
            map((result) => {
              const address: {
                formattedAddress?: string;
                displayText?: string;
                city?: string;
                state?: string;
                streetName?: string;
                streetNumber?: string;
                zip?: string;
              } = {
                formattedAddress: '',
                displayText: '',
                city: '',
                state: '',
                streetName: '',
                streetNumber: '',
                zip: '',
              };

              if (result.length > 0) {
                address.formattedAddress = result[0].formatted_address;

                const { address_components: components } = result[0];
                const includesStreetNumber = (c) =>
                  c.types.includes('street_number');
                const includesStreetName = (c) => c.types.includes('route');
                const includesCity = (c) => c.types.includes('locality');
                const includesState = (c) =>
                  c.types.includes('administrative_area_level_1');
                const includesZip = (c) => c.types.includes('postal_code');

                if (components.some(includesStreetNumber)) {
                  address.streetNumber = components.find(
                    includesStreetNumber
                  ).long_name;
                  address.displayText += address.streetNumber + ' ';
                }

                if (components.some(includesStreetName)) {
                  address.streetName = components.find(
                    includesStreetName
                  ).long_name;
                  address.displayText += address.streetName + ', ';
                }

                if (components.some(includesCity)) {
                  address.city = components.find(includesCity).long_name;
                  address.displayText += address.city + ', ';
                }

                if (components.some(includesState)) {
                  address.state = components.find(includesState).short_name;
                  address.displayText += address.state + ', ';
                }

                if (components.some(includesZip)) {
                  address.zip = components.find(includesZip).long_name;
                  address.displayText += address.zip;
                }
              }
              return actionGeocodeLocationRequestSuccess(address);
            })
          )
      )
    )
  );

  /* -------------------------------------------------------------------------- */
  /*                                  Register                                  */
  /* -------------------------------------------------------------------------- */

  // start
  effectRegisterStart = createEffect(
    () =>
      this.actions$.pipe(
        ofType(actionRegisterStart),
        tap((action) => {
          this.router.navigate(['/identity/sign-up/register'], {
            relativeTo: this.route,
          });
        })
      ),
    { dispatch: false }
  );

  // form submit
  effectRegisterFormSubmit = createEffect(() =>
    this.actions$.pipe(
      ofType(actionRegisterFormSubmit),
      withLatestFrom(this.store.select(selectSignUp)),
      map(([action, signUp]) => actionVerifyEmailRequest({ signUp }))
    )
  );

  /* -------------------------------------------------------------------------- */
  /*                                Verify Email                                */
  /* -------------------------------------------------------------------------- */

  // request
  effectVerifyEmailRequest = createEffect(() =>
    this.actions$.pipe(
      ofType(actionVerifyEmailRequest),
      switchMap((action) =>
        this.identityService.verifyEmail(action.signUp.email).pipe(
          take(1),
          map((response) =>
            actionCreateAccountRequest({ signUp: action.signUp })
          ),
          catchError((error: HttpErrorResponse) => {
            if (error.status === 400) {
              this.notification.create(
                'error',
                'Error',
                'Email already exist.',
                { nzPlacement: 'bottomRight' }
              );
            } else {
              this.notification.create('error', 'Error', error.message, {
                nzPlacement: 'bottomRight',
              });
            }
            return of(actionVerifyEmailRequestFailed(error));
          })
        )
      )
    )
  );

  /* -------------------------------------------------------------------------- */
  /*                                   SignOut                                  */
  /* -------------------------------------------------------------------------- */

  effectSignOut = createEffect(
    () =>
      this.actions$.pipe(
        ofType(actionSignOut),
        switchMap((action) => this.router.navigate(['identity', 'login']))
      ),
    { dispatch: false }
  );

  /* -------------------------------------------------------------------------- */
  /*                               Create Account                               */
  /* -------------------------------------------------------------------------- */

  // request
  effectCreateAccountRequest = createEffect(() =>
    this.actions$.pipe(
      ofType(actionCreateAccountRequest),
      switchMap((action) =>
        this.identityService.createAccount(action.signUp).pipe(
          take(1),
          map((response) => actionCreateAccountRequestSuccess({ response })),
          catchError((error) => {
            console.log(error);
            return of(actionCreateAccountRequestFailed(error));
          })
        )
      )
    )
  );

  // success
  effectCreateAccountRequestSuccess = createEffect(() =>
    this.actions$.pipe(
      ofType(actionCreateAccountRequestSuccess),
      map((action) => {
        this.router.navigate(['/identity/sign-up/account-created']);
        return actionSignInSuccess({
          response: action.response,
          redirect: false,
        });
      })
    )
  );

  // failed
  effectCreateAccountRequestFailed = createEffect(
    () =>
      this.actions$.pipe(
        ofType(actionCreateAccountRequestFailed),
        tap((action) => {
          this.router.navigate(['/identity/sign-up/account-created']);
        })
      ),
    { dispatch: false }
  );

  /* -------------------------------------------------------------------------- */
  /*                                   Sign In                                  */
  /* -------------------------------------------------------------------------- */

  // request
  effectSignInRequest = createEffect(() =>
    this.actions$.pipe(
      ofType(actionSignInRequest),
      switchMap(({ username, password }) =>
        this.identityService.signIn(username, password).pipe(
          take(1),
          tap((response) => console.log(response)),
          map((response: HttpSignInResponse) => {
            return actionSignInSuccess({ response, redirect: true });
          }),
          catchError((error: HttpErrorResponse) => {
            return of(actionSignInFailed({ error }));
          })
        )
      )
    )
  );

  // success
  effectSignInRequestSuccess = createEffect(
    () =>
      this.actions$.pipe(
        ofType(actionSignInSuccess),
        map((action) => {
          this.notification.create('success', 'Welcome', '', {
            nzPlacement: 'bottomRight',
          });
          console.log(action.response);
          if (action.redirect) {
            if (action.response.user.is_admin) {
              this.router.navigate(['admin']);
            } else {
              this.router.navigate(['storm']);
            }
          }
        })
      ),
    {
      dispatch: false,
    }
  );

  // failed
  effectSignInRequestFailed = createEffect(
    () =>
      this.actions$.pipe(
        ofType(actionSignInFailed),
        map((action) => {
          if (action.error.status === 401) {
            this.notification.create(
              'error',
              'Failed',
              'User or password not valid.',
              { nzPlacement: 'bottomRight' }
            );
          } else {
            this.notification.create('error', 'Error', action.error.message, {
              nzPlacement: 'bottomRight',
            });
          }
        })
      ),
    {
      dispatch: false,
    }
  );

  /* -------------------------------------------------------------------------- */
  /*                              Processs Payment                              */
  /* -------------------------------------------------------------------------- */

  // request
  effectProcessPaymentRequest = createEffect(() =>
    this.actions$.pipe(
      ofType(actionProcessPaymentRequest),
      switchMap((action) =>
        this.paymentService.processPayment(action.paymentInformation).pipe(
          take(1),
          map((response: HttpResponse<any>) => {
            return actionProcessPaymentRequestSuccess();
          }),
          catchError((error) => {
            return of(actionProcessPaymentRequestFailed(error));
          })
        )
      )
    )
  );

  effectProcessPaypalPaymentRequest = createEffect(
    () => {
      return this.actions$.pipe(
        ofType(actionProcessPaypalPaymentRequest),
        switchMap((action) =>
          this.paymentService.createSubscriptionFromPaypal(action.paypalPaymentInformation).pipe(
            take(1),
            map((response: PaypalCreateSubscriptionResponse) => {
              window.location.href = response.approvalUrl;
            }),
            catchError((error) => {
              return of(actionProcessPaypalPaymentRequestFailed(error));
            })
          )
        )
      );
    },
    {
      dispatch: false,
    }
  );

  // success
  effectProcessPaymentRequestSuccess = createEffect(
    () =>
      this.actions$.pipe(
        ofType(actionProcessPaymentRequestSuccess),
        map((action) => {
          this.router.navigate(['identity', 'sign-up', 'payment-successful']);
          this.notification.create(
            'success',
            'Payment',
            'Subscription has been created successfully.',
            {
              nzPlacement: 'bottomRight',
            }
          );
        })
      ),
    { dispatch: false }
  );

  // failed
  effectProcessPaymentRequestFailed = createEffect(
    () =>
      this.actions$.pipe(
        ofType(actionProcessPaymentRequestFailed),
        map((action) => {
          console.log(action.error);
          this.notification.create(
            'error',
            'Transaction Error',
            'Transaction could not be processed.',
            {
              nzPlacement: 'bottomRight',
            }
          );
        })
      ),
    { dispatch: false }
  );

  // request
  effectVerifyPaymentRequest = createEffect(() =>
    this.actions$.pipe(
      ofType(actionVerifyPayment),
      switchMap((action) =>
        this.paymentService.verifySubscriptionPayment().pipe(
          take(1),
          map((response: VerifySubscriptionPaymentResponse) => {
            return actionProcessPaymentRequestSuccess();
          }),
          catchError((error) => {
            return of(actionProcessPaymentRequestFailed(error));
          })
        )
      )
    )
  );

  /* -------------------------------------------------------------------------- */
  /*                             Update Geolocation                             */
  /* -------------------------------------------------------------------------- */

  // request
  effectUpdateGeolocationRequest = createEffect(() =>
    this.actions$.pipe(
      ofType(actionUpdateGeolocationRequest),
      switchMap((action) =>
        this.geolocationService
          .updateGeolocation(action.updateGeolocationRequestParameters)
          .pipe(
            take(1),
            map((response: HttpResponse<any>) => {
              return actionUpdateGeolocationRequestSuccess({
                newAddress: action.updateGeolocationRequestParameters,
              });
            }),
            catchError((error) => {
              this.notification.create('error', 'Error', error, {
                nzPlacement: 'bottomRight',
              });
              return of(actionUpdateGeolocationRequestFailed(error));
            })
          )
      )
    )
  );

  // success
  effectUpdateGeolocationRequestSuccess = createEffect(
    () =>
      this.actions$.pipe(
        ofType(actionUpdateGeolocationRequestSuccess),
        map((action) => {
          this.router.navigate(['storm']);
          this.notification.create(
            'success',
            'Geolocation Update',
            'User geolocation has been updated successfully.',
            {
              nzPlacement: 'bottomRight',
            }
          );
        })
      ),
    { dispatch: false }
  );

  // success
  effectUpdateGeolocationRequestFailed = createEffect(
    () =>
      this.actions$.pipe(
        ofType(actionUpdateGeolocationRequestFailed),
        map((action) => {
          this.notification.create(
            'error',
            'Geolocation Update Error',
            'User geolocation could not be updated.',
            {
              nzPlacement: 'bottomRight',
            }
          );
        })
      ),
    { dispatch: false }
  );

  constructor(
    private actions$: Actions,
    private identityService: QrIdentityService,
    private router: Router,
    private route: ActivatedRoute,
    private store: Store,
    private notification: NzNotificationService,
    private paymentService: QrPaymentService,
    private geolocationService: QrGeolocationService
  ) {}
}
