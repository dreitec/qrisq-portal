import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { NzNotificationService } from 'ng-zorro-antd/notification';
import { take } from 'rxjs/operators';
import { QrIdentityService } from '../../services/identity.service';

@Component({
  selector: 'qr-forgot-password-page',
  templateUrl: './forgot-password.component.html',
  styleUrls: ['./forgot-password.component.scss'],
})
export class QrForgotPasswordPageComponent implements OnInit {
  email = '';
  isLoading = false;
  isSent = false;
  forgotPasswordForm: FormGroup;

  constructor(
    private formBuilder: FormBuilder,
    private identityService: QrIdentityService,
    private notification: NzNotificationService
  ) {}

  ngOnInit() {
    this.forgotPasswordForm = this.formBuilder.group({
      email: ['', [Validators.required, Validators.email]],
    });
  }

  onSubmitForm($event) {
    const email = this.forgotPasswordForm.get('email').value;
    this.isLoading = true;
    this.identityService
      .forgotPassword(email)
      .pipe(take(1))
      .subscribe(
        (response) => {
          this.isLoading = false;
          this.isSent = true;
          this.email = email;
          this.forgotPasswordForm.reset({});
        },
        (error) => {
          this.isLoading = false;
          this.notification.create('error', 'Error', 'Something went wrong.');
        }
      );
  }
}
