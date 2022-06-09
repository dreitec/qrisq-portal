// angular
import { Component, OnInit } from '@angular/core';
import {
  FormBuilder,
  FormControl,
  FormGroup,
  Validators,
} from '@angular/forms';

import { select, Store } from '@ngrx/store';
import { Observable } from 'rxjs';

import { selectSignUp } from '../../store/identity.selectors';
import { actionRegisterFormSubmit } from '../../store/identity.actions';
import { SignUpState } from '../../store/identity.models';
import { ReCaptchaV3Service } from 'ng-recaptcha';

@Component({
  selector: 'qr-register-page',
  templateUrl: './register-page.component.html',
  styleUrls: ['./register-page.component.scss'],
})
export class QrRegisterPageComponent implements OnInit {
  registerForm: FormGroup;
  signUp$: Observable<SignUpState>;

  constructor(
    private fb: FormBuilder,
    private store: Store,
    private recaptchaV3Service: ReCaptchaV3Service
  ) {}

  ngOnInit(): void {
    this.signUp$ = this.store.pipe(select(selectSignUp));
    this.registerForm = this.buildFormGroup();
  }

  buildFormGroup(): FormGroup {
    const passwordFieldValidator = (
      control: FormControl
    ): { [s: string]: boolean } => {
      if (!control.value) {
        return { required: true };
      } else if (control.value !== this.registerForm.controls.password.value) {
        return { confirm: true, error: true };
      }
      return {};
    };

    const firstName = [null, [Validators.required]];
    const lastName = [null, [Validators.required]];
    const email = [null, [Validators.email, Validators.required]];
    const password = [null, [Validators.required, Validators.minLength(12)]];
    const checkPassword = [null, [Validators.required, passwordFieldValidator]];
    const phoneNumber = [null, [Validators.required]];
    const terms = [null, [Validators.required]];

    return this.fb.group({
      firstName,
      lastName,
      email,
      password,
      checkPassword,
      phoneNumber,
      terms,
    });
  }

  submitForm(): void {
    for (const i in this.registerForm.controls) {
      this.registerForm.controls[i].markAsDirty();
      this.registerForm.controls[i].updateValueAndValidity();
    }
    this.recaptchaV3Service.execute('signup')
    .subscribe((token: string) => {
      if (this.registerForm.status === 'VALID') {
        const data = {
          firstName: this.registerForm.get('firstName').value,
          lastName: this.registerForm.get('lastName').value,
          email: this.registerForm.get('email').value,
          password: this.registerForm.get('password').value,
          phoneNumber: this.registerForm.get('phoneNumber').value,
          recaptchav3Token: token,
        };
        this.store.dispatch(actionRegisterFormSubmit(data));
      }
    });
  }

  updateConfirmValidator(): void {
    /** wait for refresh value */
    Promise.resolve().then(() =>
      this.registerForm.controls.checkPassword.updateValueAndValidity()
    );
  }
}
