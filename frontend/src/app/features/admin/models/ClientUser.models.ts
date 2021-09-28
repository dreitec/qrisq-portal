export interface ClientUserTableData {
  data: ClientUserTableDataItem[];
  totalRecords: number;
  totalPages: number;
}

export interface ClientUserTableDataItem {
  id: number;
  email: string;
  firstName: string;
  lastName: string;
  address: string;
  subscriptionPlan: string;
  hasPaid: boolean;
  paymentExpired: boolean;
}

export interface ClientUser {
  id: number;
  email: string;
  firstName: string;
  lastName: string;
  profile: {
    phoneNumber: string;
    address: { lat: number; lng: number; displayText: string };
    streetNumber: string;
    city: string;
    state: string;
    zipCode: string;
    isPreprocessed: boolean;
    addressUpdated: number;
  };
  subscription_plan: {
    plan: {
      id: number;
      name: string;
      feature: string;
      price: number;
      duration: number;
    };
    subscribedOn: string;
    updatedAt: string;
    recurring: boolean;
    isCancelled: boolean;
    cancelledAt?: any;
  };
}

export interface ClientUserHttpGetResponseModel {
  id: number;
  email: string;
  first_name: string;
  last_name: string;
  has_paid: boolean;
  payment_expired: boolean;
  profile?: {
    phone_number: string;
    address?: { lat: number; lng: number; displayText: string };
    street_number: string;
    city: string;
    state: string;
    zip_code: string;
    is_preprocessed: boolean;
  };
}

export interface ClientUsersHttpGetResponseModel {
  links: any;
  results: Array<{
    id: number;
    email: string;
    first_name: string;
    last_name: string;
    has_paid: boolean;
    payment_expired: boolean;
    profile?: {
      phone_number: string;
      address?: { lat: number; lng: number; displayText: string };
      street_number: string;
      city: string;
      state: string;
      zip_code: string;
      is_preprocessed: boolean;
      address_updated: number;
    };
    subscription_plan?: {
      plan?: {
        id: number;
        name: string;
        feature: string;
        price: number;
        duration: number;
      };
      subscribed_on: string;
      updated_at: string;
      recurring: boolean;
      is_cancelled: boolean;
      cancelled_at?: any;
    };
  }>;
  total_pages: number;
  total_records: number;
}
