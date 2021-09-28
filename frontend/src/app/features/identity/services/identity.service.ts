import { Guid } from 'guid-typescript';
import { AgmGeocoder } from '@agm/core';
import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { environment } from '@env';
import { CredentialsState, SignUpState } from '../store/identity.models';
import { Observable, of } from 'rxjs';
import { catchError, map, take } from 'rxjs/operators';
import { ContactInformation } from '../models/ContactInformation';

@Injectable({
  providedIn: 'root',
})
export class QrIdentityService {
  constructor(
    private httpClient: HttpClient,
    private agmGeocoder: AgmGeocoder
  ) {}

  validateAccessToken(accessToken: string): Observable<boolean> {
    return new Observable<boolean>((observer) => {
      this.httpClient
        .get(environment.API_URL + '/auth/check-token', {
          headers: {
            'Content-type': 'application/json; charset=utf-8',
            Authorization: `Bearer ${accessToken}`,
          },
          withCredentials: true,
        })
        .pipe(
          take(1),
          catchError((error) => {
            observer.next(false);
            observer.complete();
            return of(error);
          })
        )
        .subscribe((response) => {
          observer.next(true);
          observer.complete();
        });
    });
  }

  checkServiceArea(latitude: number, longitude: number) {
    return this.httpClient.post(
      environment.API_URL + '/check-service-area',
      {
        latitude,
        longitude,
      },
      { headers: { 'Content-type': 'application/json; charset=utf-8' } }
    );
  }

  fetchSubscriptionPlans() {
    return this.httpClient
      .get(environment.API_URL + '/subscription-plans', {
        headers: { 'Content-type': 'application/json; charset=utf-8' },
      })
      .pipe(
        take(1),
        map((response: any) => response.results)
      );
  }

  geocodeLocation(lattitude: number, longitude: number) {
    const location = new google.maps.LatLng(lattitude, longitude);
    return this.agmGeocoder.geocode({ location });
  }

  createAccount(signUp: SignUpState) {
    const data = {
      email: signUp.email,
      password: signUp.password,
      confirm_password: signUp.password,
      first_name: signUp.firstName,
      last_name: signUp.lastName,
      phone_number: signUp.phoneNumber,
      address: {
        lat: signUp.lattitude,
        lng: signUp.longitude,
        displayText: signUp.addressDisplayText,
      },
      street_number: signUp.addressStreetNumber,
      city: signUp.addressCity,
      state: signUp.addressState,
      zip_code: signUp.addressZip,
      subscription_plan_id: signUp.subscriptionPlanId,
      payment_id: Guid.create().toString().substr(0, 6),
    };

    return this.httpClient.post(environment.API_URL + '/auth/signup', data, {
      headers: { 'Content-type': 'application/json; charset=utf-8' },
    });
  }

  signIn(username: string, password: string) {
    return this.httpClient.post(
      environment.API_URL + '/auth/login',
      {
        email: username,
        password,
      },
      {
        headers: { 'Content-type': 'application/json; charset=utf-8' },
      }
    );
  }

  verifyEmail(email: string) {
    return this.httpClient.post(
      environment.API_URL + '/verify-email',
      {
        email: email,
      },
      {
        headers: { 'Content-type': 'application/json; charset=utf-8' },
      }
    );
  }

  refreshCredentials(refreshToken: string) {
    return this.httpClient.post(
      environment.API_URL + '/auth/refresh',
      { refresh: refreshToken },
      {
        headers: { 'Content-type': 'application/json; charset=utf-8' },
      }
    );
  }

  signOut(refreshToken: string) {
    return this.httpClient.post(
      environment.API_URL + '/auth/logout',
      { refresh: refreshToken },
      {
        headers: { 'Content-type': 'application/json; charset=utf-8' },
      }
    );
  }

  getContactInformation() {
    return this.httpClient.get(environment.API_URL + '/auth/account-profile', {
      headers: { 'Content-type': 'application/json; charset=utf-8' },
    });
  }

  updateContactInformation(contactInformation: ContactInformation) {
    return this.httpClient.post(
      environment.API_URL + '/auth/account-profile',
      contactInformation,
      {
        headers: { 'Content-type': 'application/json; charset=utf-8' },
      }
    );
  }

  forgotPassword(email: string) {
    return this.httpClient.post(
      environment.API_URL + '/auth/forgot-password',
      {
        email,
      },
      {
        headers: { 'Content-type': 'application/json; charset=utf-8' },
      }
    );
  }

  resetPassword(
    {
      newPassword,
      confirmNewPassword,
    }: { newPassword: string; confirmNewPassword: string },
    token: string,
    uid: string
  ) {
    return this.httpClient.post(
      environment.API_URL + '/auth/reset-password/' + uid + '/' + token,
      {
        new_password: newPassword,
        confirm_password: confirmNewPassword,
      },
      {
        headers: { 'Content-type': 'application/json; charset=utf-8' },
      }
    );
  }

  cancelSubscription() {
    return this.httpClient.post(
      environment.API_URL + '/cancel-subscription',
      {},
      {
        headers: { 'Content-type': 'application/json; charset=utf-8' },
      }
    );
  }

  getAccountProfile() {
    return this.httpClient.get(environment.API_URL + '/auth/account-profile', {
      headers: { 'Content-type': 'application/json; charset=utf-8' },
    });
  }
}
