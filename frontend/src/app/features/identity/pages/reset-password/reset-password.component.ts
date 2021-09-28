import { Router, ActivatedRoute } from '@angular/router';
import { NzNotificationService } from 'ng-zorro-antd/notification';
import { Component, OnInit } from '@angular/core';
import {
  FormBuilder,
  FormControl,
  FormGroup,
  Validators,
} from '@angular/forms';
import { QrIdentityService } from '../../services/identity.service';
import { take } from 'rxjs/operators';

@Component({
  selector: 'qr-reset-password-password',
  templateUrl: './reset-password.component.html',
  styleUrls: ['./reset-password.component.scss'],
})
export class QrResetPasswordPageComponent implements OnInit {
  isLoading = false;
  resetPasswordForm: FormGroup;
  token: string;
  uid: string;

  constructor(
    private formBuilder: FormBuilder,
    private identityService: QrIdentityService,
    private notification: NzNotificationService,
    private router: Router,
    private route: ActivatedRoute
  ) {}

  ngOnInit() {
    this.route.queryParams.pipe(take(1)).subscribe((params) => {
      console.log(params);
      this.token = params.token;
      this.uid = params.uid;
    });

    this.resetPasswordForm = this.buildResetPasswordForm();
  }

  onSubmitForm($event) {
    this.isLoading = true;
    const newPassword = this.resetPasswordForm.get('newPassword').value;
    const confirmNewPassword = this.resetPasswordForm.get('confirmNewPassword')
      .value;

    this.identityService
      .resetPassword({ newPassword, confirmNewPassword }, this.token, this.uid)
      .pipe(take(1))
      .subscribe(
        (response) => {
          this.isLoading = false;
          this.notification.create(
            'success',
            'Reset Password',
            'Your password was changed successfully. You will be redirected to the login page.',
            { nzPlacement: 'bottomRight' }
          );
          this.router.navigate(['identity', 'login']);
        },
        (error) => {
          this.isLoading = false;
          this.notification.create('error', 'Error', 'Something went wrong.');
        }
      );
  }

  buildResetPasswordForm() {
    const newPasswordFieldValidator = (
      control: FormControl
    ): { [s: string]: boolean } => {
      if (!control.value) {
        return { required: true };
      } else if (
        control.value !== this.resetPasswordForm.get('newPassword').value
      ) {
        return { confirm: true, error: true };
      }
      return {};
    };

    return this.formBuilder.group({
      newPassword: [
        '',
        [
          Validators.required,
          Validators.pattern(
            /^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$/
          ),
        ],
      ],
      confirmNewPassword: [
        '',
        [Validators.required, newPasswordFieldValidator],
      ],
    });
  }

  updateConfirmNewPasswordValidator(): void {
    /** wait for refresh value */
    Promise.resolve().then(() =>
      this.resetPasswordForm.get('confirmNewPassword').updateValueAndValidity()
    );
  }
}
