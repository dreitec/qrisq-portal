// angular
import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';

// rxjs
import { Observable } from 'rxjs';
import { take } from 'rxjs/operators';

// schema

// environment
import { environment } from '@env';
import { AgmGeocoder } from '@agm/core';

// models
import { GeocodedAddress } from '../models/Geocoding.models';

@Injectable({
  providedIn: 'root',
})
export class QrGeocodingService {
  constructor(
    private httpClient: HttpClient,
    private agmGeocoder: AgmGeocoder
  ) {}

  geocodeLocation(lat: number, lng: number): Observable<GeocodedAddress> {
    return new Observable((observer) => {
      // reverse geocoding
      const location = new google.maps.LatLng(lat, lng);
      this.agmGeocoder
        .geocode({ location })
        .pipe(take(1))
        .subscribe((result) => {
          if (result.length > 0) {
            let address: GeocodedAddress = {
              displayText: '',
              city: '',
              state: '',
              streetName: '',
              streetNumber: '',
              zipCode: '',
              lattitude: lat,
              longitude: lng,
              formattedAddress: '',
            };

            address.formattedAddress = result[0].formatted_address;

            const { address_components: components } = result[0];
            const includesStreetNumber = (c) =>
              c.types.includes('street_number');
            const includesStreetName = (c) => c.types.includes('route');
            const includesCity = (c) => c.types.includes('locality');
            const includesState = (c) =>
              c.types.includes('administrative_area_level_1');
            const includesZip = (c) => c.types.includes('postal_code');

            if (components.some(includesStreetNumber)) {
              address.streetNumber = components.find(
                includesStreetNumber
              ).long_name;
              address.displayText += address.streetNumber + ' ';
            }

            if (components.some(includesStreetName)) {
              address.streetName = components.find(
                includesStreetName
              ).long_name;
              address.displayText += address.streetName + ', ';
            }

            if (components.some(includesCity)) {
              address.city = components.find(includesCity).long_name;
              address.displayText += address.city + ', ';
            }

            if (components.some(includesState)) {
              address.state = components.find(includesState).short_name;
              address.displayText += address.state + ', ';
            }

            if (components.some(includesZip)) {
              address.zipCode = components.find(includesZip).long_name;
              address.displayText += address.zipCode;
            }

            observer.next(address);
          }
        });
    });
  }
}
