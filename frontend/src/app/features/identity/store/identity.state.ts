import { IdentityState } from './identity.models';

export const initialState: IdentityState = {
  signUp: null,
  signIn: null,
  credentials: null,
  signedUser: null,
  errors: [],
  loading: false,
  payment: {
    paymentFailed: false,
  },
};
