// angular
import { HttpErrorResponse, HttpResponse } from '@angular/common/http';

// ngrx
import { createAction, props } from '@ngrx/store';

// models
import { GeocodedAddress } from '../models/Geocoding.models';
import { HttpSignInResponse } from '../models/HttpSignInResponse.models';
import {
  PaymentInformation,
  PaypalPaymentInformation,
} from '../models/Payment.models';
import { UpdateGeolocationRequestParameters } from '../models/UpdateGeolocation.models';
import { SignUpState } from './identity.models';

/* -------------------------------------------------------------------------- */
/*                             Check Service Area                             */
/* -------------------------------------------------------------------------- */

// request

export const actionCheckServiceAreaRequest = createAction(
  '[Identity] Check Service Area Request',
  props<{ lattitude: number; longitude: number }>()
);

// success

export const actionCheckServiceAreaRequestSuccess = createAction(
  '[Identity] Check Service Area Request Success',
  props<{ available: boolean; services: Array<string> }>()
);

// failed

export const actionCheckServiceAreaRequestFailed = createAction(
  '[Identity] Check Service Area Request Failed',
  props<{ error: HttpErrorResponse }>()
);

/* -------------------------------------------------------------------------- */
/*                                Service Area                                */
/* -------------------------------------------------------------------------- */

// available
export const actionServiceAreaAvailable = createAction(
  '[Identity] Service Area Available',
  props<{ onlyWind: boolean }>()
);

// unavailable
export const actionServiceAreaUnavailable = createAction(
  '[Identity] Service Area Unavailable'
);

/* -------------------------------------------------------------------------- */
/*                              Geocode Location                              */
/* -------------------------------------------------------------------------- */

// request
export const actionGeocodeLocationRequest = createAction(
  '[Identity] Geocode Location Request',
  props<{ lattitude: number; longitude: number }>()
);

// success
export const actionGeocodeLocationRequestSuccess = createAction(
  '[Identity] Geocode Location Request Success',
  props<{
    formattedAddress?: string;
    displayText?: string;
    city?: string;
    state?: string;
    streetName?: string;
    streetNumber?: string;
    zip?: string;
  }>()
);

// failed
export const actionGeocodeLocationRequestFailed = createAction(
  '[Identity] Geocode Location Request Failed'
);

/* -------------------------------------------------------------------------- */
/*                                  Register                                  */
/* -------------------------------------------------------------------------- */

// start
export const actionRegisterStart = createAction(
  '[Identity] Register Start',
  props<{
    subscriptionPlanId: number;
  }>()
);

// form submit
export const actionRegisterFormSubmit = createAction(
  '[Identity] Register Form Submit',
  props<{
    firstName: string;
    lastName: string;
    email: string;
    password: string;
    phoneNumber: string;
  }>()
);

/* -------------------------------------------------------------------------- */
/*                                Verify Email                                */
/* -------------------------------------------------------------------------- */

// request
export const actionVerifyEmailRequest = createAction(
  '[Identity] Verify Email Request',
  props<{
    signUp: SignUpState;
  }>()
);

// success
export const actionVerifyEmailRequestSuccess = createAction(
  '[Identity] Verify Email Request Success'
);

// failed
export const actionVerifyEmailRequestFailed = createAction(
  '[Identity] Verify Email Request Failed',
  props<{ error: HttpErrorResponse }>()
);

/* -------------------------------------------------------------------------- */
/*                               Create Account                               */
/* -------------------------------------------------------------------------- */

// request
export const actionCreateAccountRequest = createAction(
  '[Identity] Create Account Request',
  props<{
    signUp: SignUpState;
  }>()
);

// success
export const actionCreateAccountRequestSuccess = createAction(
  '[Identity] Create Account Request Success',
  props<{ response }>()
);

// failed
export const actionCreateAccountRequestFailed = createAction(
  '[Identity] Create Account Request Failed',
  props<{ error: HttpErrorResponse }>()
);

/* -------------------------------------------------------------------------- */
/*                                   Sign In                                  */
/* -------------------------------------------------------------------------- */

// request
export const actionSignInRequest = createAction(
  '[Identity] Sign In Request',
  props<{ username: string; password: string }>()
);

// success
export const actionSignInSuccess = createAction(
  '[Identity] Sign In Success',
  props<{ response: HttpSignInResponse; redirect: boolean }>()
);

// failed
export const actionSignInFailed = createAction(
  '[Identity] Sign In Failed',
  props<{ error: HttpErrorResponse }>()
);

/* -------------------------------------------------------------------------- */
/*                                   SignUp                                   */
/* -------------------------------------------------------------------------- */

export const actionSignUpAddressChanged = createAction(
  '[Identity] Sign In Address Changed',
  props<{ address: GeocodedAddress }>()
);

/* -------------------------------------------------------------------------- */
/*                                Access Token                                */
/* -------------------------------------------------------------------------- */

export const actionAccessTokenRefreshed = createAction(
  '[Identity] Access Token Refreshed',
  props<{ newAccessToken: string }>()
);

/* -------------------------------------------------------------------------- */
/*                                   SignOut                                  */
/* -------------------------------------------------------------------------- */

export const actionSignOut = createAction(
  '[Identity] Sign Out',
  props<{ refreshToken: string }>()
);

/* -------------------------------------------------------------------------- */
/*                                   Payment                                  */
/* -------------------------------------------------------------------------- */

// request
export const actionResetPayment = createAction(
  '[Identity] Process Reset Payment'
);

// request
export const actionProcessPaymentRequest = createAction(
  '[Identity] Process Payment Request',
  props<{ paymentInformation: PaymentInformation }>()
);

// success
export const actionProcessPaymentRequestSuccess = createAction(
  '[Identity] Process Payment Request Success',
);

// failed
export const actionProcessPaymentRequestFailed = createAction(
  '[Identity] Process Payment Request Failed',
  props<{ error: HttpErrorResponse }>()
);

// request
export const actionProcessPaypalPaymentRequest = createAction(
  '[Identity] Process Paypal Payment Request',
  props<{ paypalPaymentInformation: PaypalPaymentInformation }>()
);

// success
export const actionProcessPaypalPaymentRequestSuccess = createAction(
  '[Identity] Process Paypal Payment Request Success'
);

// failed
export const actionProcessPaypalPaymentRequestFailed = createAction(
  '[Identity] Process Paypal Payment Request Failed',
  props<{ error: HttpErrorResponse }>()
);

/* -------------------------------------------------------------------------- */
/*                             Update Geolocation                             */
/* -------------------------------------------------------------------------- */
// request
export const actionUpdateGeolocationRequest = createAction(
  '[Identity] Update Geolocation Request',
  props<{
    updateGeolocationRequestParameters: UpdateGeolocationRequestParameters;
  }>()
);

// success
export const actionUpdateGeolocationRequestSuccess = createAction(
  '[Identity] Update Geolocation Request Success',
  props<{ newAddress: UpdateGeolocationRequestParameters }>()
);

// failed
export const actionUpdateGeolocationRequestFailed = createAction(
  '[Identity] Update Geolocation Request Failed',
  props<{ error: HttpErrorResponse }>()
);

/* -------------------------------------------------------------------------- */
/*                                 Credentials                                */
/* -------------------------------------------------------------------------- */
