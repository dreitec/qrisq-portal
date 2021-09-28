export interface HttpSignInResponse {
  refresh: string;
  access: string;
  user: User;
}

export interface User {
  id: number;
  email: string;
  first_name: string;
  last_name: string;
  profile: Profile;
  subscription: Subscription;
  has_paid?: any;
  is_admin?: boolean;
}

export interface Subscription {
  plan: Plan;
  recurring: boolean;
  is_cancelled: boolean;
  cancelled_at?: any;
}

export interface Plan {
  id: number;
  name: string;
  feature: string;
  price?: any;
  duration?: any;
}

export interface Profile {
  phone_number: string;
  address: Address;
  street_number: string;
  city: string;
  state: string;
  zip_code: string;
  is_preprocessed: boolean;
  address_updated: number;
}

export interface Address {
  lat: number;
  lng: number;
  displayText: string;
}
