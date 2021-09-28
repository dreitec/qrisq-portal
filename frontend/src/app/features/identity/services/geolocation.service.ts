import { AgmGeocoder } from '@agm/core';
import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { environment } from '@env';
import { UpdateGeolocationRequestParameters } from '../models/UpdateGeolocation.models';

@Injectable({
  providedIn: 'root',
})
export class QrGeolocationService {
  constructor(private httpClient: HttpClient) {}

  updateGeolocation(parameters: UpdateGeolocationRequestParameters) {
    return this.httpClient.post(
      environment.API_URL + '/pin-drag-address',
      parameters,
      {
        withCredentials: true,
        headers: { 'Content-type': 'application/json; charset=utf-8' },
      }
    );
  }

  getPinDragAttemptCounter() {
    return this.httpClient.get(environment.API_URL + '/pin-drag-attempt', {
      withCredentials: true,
      headers: { 'Content-type': 'application/json; charset=utf-8' },
    });
  }

  incrementPinDragAttemptCounter() {
    return this.httpClient.post(
      environment.API_URL + '/pin-drag-attempt',
      {},
      {
        withCredentials: true,
        headers: { 'Content-type': 'application/json; charset=utf-8' },
      }
    );
  }

  sendPinDragAttemptsExceededEmail() {
    return this.httpClient.post(
      environment.API_URL + '/request-address-change',
      {},
      {
        withCredentials: true,
        headers: { 'Content-type': 'application/json; charset=utf-8' },
      }
    );
  }
}
