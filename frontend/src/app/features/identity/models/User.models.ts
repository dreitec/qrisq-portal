export interface User {
  id?: number;
  email?: string;
  firstName?: string;
  lastName?: string;
  hasPaid?: any;
  phoneNumber?: string;
  geolocation?: UserGeoLocation;
  address?: UserAddress;
  subscription?: UserSubscription;
  isPreprocessed?: boolean;
  addressUpdated?: number;
  isAdmin?: boolean;
}

export interface UserSubscription {
  id: number;
  name: string;
  feature: string;
  price?: any;
  duration?: any;
  recurring: boolean;
  isCancelled: boolean;
  cancelled_at?: any;
}

export interface UserAddress {
  displayText: string;
  streetNumber: string;
  city: string;
  state: string;
  zipCode: string;
}

export interface UserGeoLocation {
  lattitude: number;
  longitude: number;
}
