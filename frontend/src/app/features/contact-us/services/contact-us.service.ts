import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { environment } from '@env';
@Injectable({
  providedIn: 'root',
})
export class QrContactUsService {
  constructor(private httpClient: HttpClient) {}

  submit(firstName, lastName, email, message) {
    return this.httpClient.post(
      environment.API_URL + '/send-message',
      { name: firstName + ' ' + lastName, email, message },
      { headers: { 'Content-type': 'application/json; charset=utf-8' } }
    );
  }
}
