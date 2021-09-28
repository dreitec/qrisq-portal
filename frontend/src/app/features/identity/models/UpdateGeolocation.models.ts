export interface UpdateGeolocationRequestParameters {
  address: {
    lat: number;
    lng: number;
    displayText: string;
  };
  street_number: string;
  city: string;
  state: string;
  zip_code: string;
}
