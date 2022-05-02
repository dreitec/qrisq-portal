import { createSelector, Store } from '@ngrx/store';
import { Component, OnInit } from '@angular/core';

import {
  FormBuilder,
  FormControl,
  FormGroup,
  Validators,
} from '@angular/forms';

import { Router } from '@angular/router';
import { NzNotificationService } from 'ng-zorro-antd/notification';
import { actionSignInRequest } from '../../store/identity.actions';
import { selectSignIn } from '../../store/identity.selectors';
import { HttpErrorResponse } from '@angular/common/http';
import { SignInState } from '../../store/identity.models';

@Component({
  selector: 'qr-login-page',
  templateUrl: './login-page.component.html',
  styleUrls: ['./login-page.component.scss'],
})
export class QrLoginPageComponent implements OnInit {
  loginForm!: FormGroup;

  constructor(
    private fb: FormBuilder,
    private router: Router,
    private notification: NzNotificationService,
    private store: Store
  ) {}

  ngOnInit(): void {
    this.loginForm = this.buildForm();
  }

  buildForm(): FormGroup {
    return this.fb.group({
      username: [null, [Validators.required, Validators.email]],
      password: [null, [Validators.required]],
    });
  }

  submitForm(): void {
    for (const i in this.loginForm.controls) {
      this.loginForm.controls[i].markAsDirty();
      this.loginForm.controls[i].updateValueAndValidity();
    }
    if (this.loginForm.valid) {
      this.store.dispatch(
        actionSignInRequest({
          username: this.loginForm.get('username').value,
          password: this.loginForm.get('password').value,
        })
      );
    }
  }

  onRegisterClick($event) {
    this.router.navigate(['identity', 'sign-up']);
  }

  onForgotPasswordClick($event) {
    this.router.navigate(['identity', 'forgot-password']);
  }
}
