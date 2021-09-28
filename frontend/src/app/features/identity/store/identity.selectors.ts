// ngrx
import { RootState } from '@app/core/store/state';
import { createFeatureSelector, createSelector } from '@ngrx/store';
import { CredentialsState, IdentityState } from './identity.models';

export const selectIdentityState = createFeatureSelector<
  RootState,
  IdentityState
>('identity');

// signUp
export const selectSignUp = createSelector(
  selectIdentityState,
  (state: IdentityState) => state.signUp
);

export const selectSignIn = createSelector(
  selectIdentityState,
  (state: IdentityState) => state.signIn
);

export const selectPayment = createSelector(
  selectIdentityState,
  (state: IdentityState) => state.payment
);

export const selectCredentials = createSelector(
  selectIdentityState,
  (state: IdentityState) => state.credentials
);

export const selectSignedUser = createSelector(
  selectIdentityState,
  (state: IdentityState) => state.signedUser
);
