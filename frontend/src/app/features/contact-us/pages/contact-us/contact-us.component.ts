// angular
import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { QrContactUsService } from '@app/features/contact-us/services/contact-us.service';
import { of } from 'rxjs';
import { catchError, take } from 'rxjs/operators';
import { NzNotificationService } from 'ng-zorro-antd/notification';

@Component({
  selector: 'qr-contact-us-page',
  templateUrl: './contact-us.component.html',
  styleUrls: ['./contact-us.component.scss'],
})
export class QrContactUsPageComponent implements OnInit {
  isLoading: boolean;

  // form
  contactUsForm: FormGroup = this.formBuilder.group({
    firstName: ['', [Validators.required, Validators.max(10)]],
    lastName: ['', [Validators.required, Validators.max(10)]],
    email: ['', [Validators.required, Validators.email]],
    message: ['', [Validators.required, Validators.max(200)]],
  });

  constructor(
    private formBuilder: FormBuilder,
    private contactUsService: QrContactUsService,
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

    const { firstName, lastName, email, message } = this.contactUsForm.value;
    this.isLoading = true;
    this.contactUsService
      .submit(firstName, lastName, email, message)
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
}
