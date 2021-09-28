import { HttpClient } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { environment } from '@env';
import { of } from 'rxjs';
import { catchError, take } from 'rxjs/operators';
import { NzNotificationService } from 'ng-zorro-antd/notification';

@Component({
  selector: 'qr-contact-us-form',
  templateUrl: './contact-us.component.html',
  styleUrls: ['./contact-us.component.scss'],
})
export class QrContactUsFormComponent implements OnInit {
  // form
  contactUsForm: FormGroup = this.formBuilder.group({
    name: ['', [Validators.required, Validators.max(10)]],
    email: ['', [Validators.required, Validators.email]],
    message: ['', [Validators.required, Validators.max(200)]],
  });

  isLoading: boolean;

  constructor(
    private formBuilder: FormBuilder,
    private httpClient: HttpClient,
    private notification: NzNotificationService
  ) {}

  ngOnInit() {}

  onSubmitForm($event) {
    for (const i in this.contactUsForm.controls) {
      this.contactUsForm.controls[i].markAsDirty();
      this.contactUsForm.controls[i].updateValueAndValidity();
    }
    if (!this.contactUsForm.valid) {
      return;
    }
    this.isLoading = true;
    const { name, email, message } = this.contactUsForm.value;
    this.submit(name, email, message)
      .pipe(
        take(1),
        catchError((error) => {
          this.notification.create('error', 'Error', 'Something went wrong.');
          return of(error);
        })
      )
      .subscribe((response) => {
        this.isLoading = false;
        this.notification.create(
          'success',
          'Thank you',
          'Your message has been successfully sent.',
          { nzPlacement: 'bottomRight' }
        );
        this.contactUsForm.reset({});
      });
  }

  submit(name, email, message) {
    return this.httpClient.post(
      environment.API_URL + '/send-message',
      { name: name, email, message },
      { headers: { 'Content-type': 'application/json; charset=utf-8' } }
    );
  }
}
