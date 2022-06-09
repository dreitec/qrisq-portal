import { HttpErrorResponse } from '@angular/common/http';
import { User } from '../models/User.models';

//
// IdentityState
//
export interface IdentityState {
  signUp: SignUpState;
  signIn: SignInState;
  credentials: CredentialsState;
  signedUser: SignedUserState;
  errors: Array<HttpErrorResponse>;
  loading: boolean;
  payment: {
    paymentFailed: boolean;
  };
}

//
// IdentityStateSignUp
//
export interface SignUpState {
  lattitude?: number;
  longitude?: number;
  email?: string;
  firstName?: string;
  lastName?: string;
  password?: string;
  windServiceOnly?: boolean;
  phoneNumber?: string;
  subscriptionPlanId?: number;
  subscriptionPlanName?: string;
  subscriptionPlanPrice?: number;
  paymentId?: string;
  addressFormatted?: string;
  addressDisplayText?: string;
  addressStreetName?: string;
  addressStreetNumber?: string;
  addressLine1?: string;
  addressLine2?: string;
  addressCity?: string;
  addressState?: string;
  addressZip?: string;
  recaptchav3Token?: string;
}

export interface CredentialsState {
  userId: number;
  accessToken: string;
  refreshToken: string;
}

//
// IdentityStateSignIn
//
export interface SignInState {
  username: string;
  password: string;
  requested: boolean;
  succeeded: boolean;
  failed: boolean;
  error: HttpErrorResponse;
}

export interface SignedUserState {
  user: User;
}

export interface IdentitySignedUserAddressState {
  displayText: string;
  phoneNumber: string;
  streetNumber: string;
  city: string;
  state: string;
  zipCode: string;
}

export interface IdentitySignedUserGeoLocationState {
  lattitude: number;
  longitude: number;
}
