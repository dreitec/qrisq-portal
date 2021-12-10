import { Action, createReducer, on } from '@ngrx/store';
import { HttpSignInResponse } from '../models/HttpSignInResponse.models';

import {
  actionAccessTokenRefreshed,
  actionCheckServiceAreaRequest,
  actionCheckServiceAreaRequestSuccess,
  actionCreateAccountRequest,
  actionCreateAccountRequestFailed,
  actionCreateAccountRequestSuccess,
  actionGeocodeLocationRequest,
  actionGeocodeLocationRequestFailed,
  actionGeocodeLocationRequestSuccess,
  actionProcessPaymentRequestFailed,
  actionProcessPaymentRequestSuccess,
  actionProcessPaypalPaymentRequest,
  actionRegisterFormSubmit,
  actionRegisterStart,
  actionResetPayment,
  actionServiceAreaAvailable,
  actionServiceAreaUnavailable,
  actionSignInFailed,
  actionSignInRequest,
  actionSignInSuccess,
  actionSignOut,
  actionSignUpAddressChanged,
  actionVerifyEmailRequest,
  actionVerifyEmailRequestFailed,
  actionVerifyEmailRequestSuccess,
} from './identity.actions';
import { IdentityState } from './identity.models';

import { initialState } from './identity.state';
import {
  actionProcessPaymentRequest,
  actionUpdateGeolocationRequest,
  actionUpdateGeolocationRequestSuccess,
} from './identity.actions';

const reducer = createReducer(
  initialState,
  on(actionCheckServiceAreaRequest, (state, { lattitude, longitude }) => ({
    ...state,
    signUp: { lattitude, longitude },
    loading: true,
  })),
  on(actionCheckServiceAreaRequestSuccess, (state) => ({
    ...state,
    loading: false,
  })),
  on(actionServiceAreaAvailable, (state, { onlyWind }) => ({
    ...state,
    signUp: { ...state.signUp, windServiceOnly: onlyWind },
    loading: false,
  })),
  on(actionServiceAreaUnavailable, (state) => ({
    ...state,
    signUp: null,
    loading: false,
  })),
  on(actionGeocodeLocationRequest, (state) => ({ ...state })),
  on(actionGeocodeLocationRequestSuccess, (state, address) => ({
    ...state,
    signUp: {
      ...state.signUp,
      addressFormatted: address.formattedAddress,
      addressDisplayText: address.displayText,
      addressStreetName: address.streetName,
      addressStreetNumber: address.streetNumber,
      addressCity: address.city,
      addressState: address.state,
      addressZip: address.zip,
    },
  })),
  on(actionGeocodeLocationRequestFailed, (state) => ({
    ...state,
    signup: {
      ...state.signUp,
      addressFormatted: 'error en geocodificado',
      addressDisplayText: 'error en geocodificado',
      addressStreetName: '',
      addressStreetNumber: '',
      addressCity: '',
      addressState: '',
      addressZip: '',
    },
  })),
  on(actionRegisterStart, (state, { subscriptionPlanId }) => ({
    ...state,
    signUp: { ...state.signUp, subscriptionPlanId },
  })),
  on(
    actionRegisterFormSubmit,
    (state, { firstName, lastName, email, password, phoneNumber }) => ({
      ...state,
      signUp: {
        ...state.signUp,
        firstName,
        lastName,
        email,
        password,
        phoneNumber,
      },
    })
  ),
  on(actionCreateAccountRequest, (state) => ({
    ...state,
    loading: true,
  })),
  on(actionCreateAccountRequestSuccess, (state) => ({
    ...state,
    signUp: null,
    loading: false,
  })),
  on(actionCreateAccountRequestFailed, (state) => ({
    ...state,
    loading: false,
  })),

  //
  // SignIn Request
  //
  on(actionSignInRequest, (state, { username, password }) => ({
    ...state,
    signIn: {
      username,
      password,
      requested: true,
      succeeded: false,
      failed: false,
      error: null,
    },
  })),

  //
  // SignIn Success
  //
  on(actionSignInSuccess, (state, { response }) => ({
    ...state,
    signIn: {
      username: null,
      password: null,
      requested: false,
      succeeded: true,
      failed: false,
      error: null,
    },
    signedUser: {
      ...state.signedUser,
      user: {
        id: response.user.id,
        firstName: response.user.first_name,
        lastName: response.user.last_name,
        email: response.user.email,
        isAdmin: response.user.is_admin,
        geolocation: response.user.profile
          ? {
              lattitude: response.user.profile.address.lat,
              longitude: response.user.profile.address.lng,
            }
          : { lattitude: 0, longitude: 0 },
        address: response.user.profile
          ? {
              displayText: response.user.profile.address.displayText,
              streetNumber: response.user.profile.street_number,
              city: response.user.profile.city,
              state: response.user.profile.state,
              zipCode: response.user.profile.zip_code,
            }
          : {
              displayText: '',
              streetNumber: '',
              city: '',
              state: '',
              zipCode: '',
            },
        phoneNumber: response.user.profile
          ? response.user.profile.phone_number
          : '',
        isPreprocessed: response.user.profile
          ? response.user.profile.is_preprocessed
          : false,
        addressUpdated: response.user.profile
          ? response.user.profile.address_updated
          : 0,
        subscription: response.user.subscription
          ? {
              id: response.user.subscription.plan.id,
              name: response.user.subscription.plan.name,
              feature: response.user.subscription.plan.feature,
              isCancelled: response.user.subscription.is_cancelled,
              recurring: response.user.subscription.recurring,
              cancelled_at: response.user.subscription.cancelled_at,
              duration: response.user.subscription.plan.duration,
              price: response.user.subscription.plan.price,
            }
          : {
              id: 0,
              name: '',
              feature: '',
              isCancelled: false,
              recurring: false,
              cancelled_at: null,
              duration: null,
              price: 0,
            },
        hasPaid: response.user.has_paid,
      },
    },
    credentials: {
      userId: response.user.id,
      accessToken: response.access,
      refreshToken: response.refresh,
      isAuthenticated: true,
    },
  })),

  //
  // SignIn Failed
  //
  on(actionSignInFailed, (state, { error }) => ({
    ...state,
    signIn: {
      ...state.signIn,
      password: '',
      requested: false,
      succeeded: false,
      failed: true,
      error,
    },
  })),

  //
  // Verify Email Request
  //
  on(actionVerifyEmailRequest, (state) => ({
    ...state,
    loading: true,
  })),

  //
  // Verify Email Request Success
  //
  on(actionVerifyEmailRequestSuccess, (state) => ({
    ...state,
    loading: false,
  })),

  //
  // Verify Email Request Failed
  //
  on(actionVerifyEmailRequestFailed, (state) => ({
    ...state,
    loading: false,
  })),

  // SignUp Address Changed
  on(actionSignUpAddressChanged, (state, { address }) => ({
    ...state,
    signUp: {
      ...state.signUp,
      lattitude: address.lattitude,
      longitude: address.longitude,
      addressFormatted: address.formattedAddress,
      addressDisplayText: address.displayText,
      addressStreetNumber: address.streetNumber,
      addressStreetName: address.displayText,
      addressCity: address.city,
      addressState: address.state,
      addressZip: address.zipCode,
    },
  })),

  //
  // Access Token Refreshed
  //
  on(actionAccessTokenRefreshed, (state, { newAccessToken }) => ({
    ...state,
    credentials: {
      ...state.credentials,
      access: newAccessToken,
    },
  })),

  //
  // SignOut
  //
  on(actionSignOut, (state, { refreshToken }) => ({
    ...state,
    signedUser: null,
    credentials: null,
  })),

  // Payment

  on(actionResetPayment, (state) => ({
    ...state,
    payment: {
      paymentFailed: false,
    },
  })),

  on(actionProcessPaymentRequest, (state, { paymentInformation }) => ({
    ...state,
    payment: {
      paymentFailed: false,
    },
    user: {
      ...state.signedUser.user,
      hasPaid: true,
    }
  })),

  on(actionProcessPaymentRequestSuccess, (state) => ({
    ...state,
    signedUser: {
      ...state.signedUser,
      user: {
        ...state.signedUser.user,
        hasPaid: true,
      },
    },
  })),

  on(actionProcessPaymentRequestFailed, (state) => ({
    ...state,
    payment: {
      paymentFailed: true,
    },
  })),

  on(actionProcessPaypalPaymentRequest, (state) => ({
    ...state,
    signedUser: {
      ...state.signedUser,
      user: {
        ...state.signedUser.user,
        hasPaid: true,
      },
    },
  })),

  on(actionUpdateGeolocationRequestSuccess, (state, { newAddress }) => ({
    ...state,
    signedUser: {
      ...state.signedUser,
      user: {
        ...state.signedUser.user,
        address: {
          city: newAddress.city,
          state: newAddress.state,
          streetNumber: newAddress.street_number,
          zipCode: newAddress.zip_code,
          displayText: newAddress.address.displayText,
        },
        geolocation: {
          lattitude: newAddress.address.lat,
          longitude: newAddress.address.lng,
        },
        addressUpdated: 1,
      },
    },
  }))
);

export function IdentityReducer(
  state: IdentityState | undefined,
  action: Action
): IdentityState {
  return reducer(state, action);
}
