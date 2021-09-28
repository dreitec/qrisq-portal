export interface GeocodedAddress {
  lattitude: number;
  longitude: number;
  displayText: string;
  streetNumber: string;
  streetName: string;
  city: string;
  state: string;
  zipCode: string;
  formattedAddress: string;
}
