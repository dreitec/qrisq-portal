import { Component, OnInit } from '@angular/core';
import {
  AbstractControl,
  FormBuilder,
  FormControl,
  FormGroup,
  ValidationErrors,
  ValidatorFn,
  Validators,
} from '@angular/forms';
import { Store } from '@ngrx/store';
import { NzNotificationService } from 'ng-zorro-antd/notification';
import { Observable, of, pipe } from 'rxjs';
import { catchError, map, take } from 'rxjs/operators';
import { ContactInformation } from '../../models/ContactInformation';
import { QrIdentityService } from '../../services/identity.service';
import { selectSignedUser } from '../../store/identity.selectors';
import { SignedUserState } from '../../store/identity.models';

@Component({
  selector: 'qr-contact-information-page',
  templateUrl: './contact-information.component.html',
  styleUrls: ['./contact-information.component.scss'],
})
export class QrContactInformationPageComponent implements OnInit {
  isLoading = false;
  updateEmail = false;
  updatePhoneNumber = false;
  updatePassword = false;

  signedUser$ = this.store.select(selectSignedUser);

  contactInformationForm: FormGroup;

  constructor(
    private formBuilder: FormBuilder,
    private identityService: QrIdentityService,
    private notification: NzNotificationService,
    private store: Store
  ) {}

  ngOnInit() {
    this.signedUser$.subscribe((signedUser: SignedUserState) => {
      if (signedUser) {
        this.contactInformationForm = this.buildFormGroup(signedUser);
      }
    });
  }

  buildFormGroup(signedUser: SignedUserState): FormGroup {
    const newEmailFieldValidator = (
      control: FormControl
    ): { [s: string]: boolean } => {
      if (!control.value) {
        return { required: true };
      } else if (
        control.value !==
        this.contactInformationForm.get('email.newEmail').value
      ) {
        return { confirm: true, error: true };
      }
      return {};
    };

    const newPhoneFieldValidator = (
      control: FormControl
    ): { [s: string]: boolean } => {
      if (!control.value) {
        return { required: true };
      } else if (
        control.value !==
        this.contactInformationForm.get('phoneNumber.newPhoneNumber').value
      ) {
        return { confirm: true, error: true };
      }
      return {};
    };

    const newPasswordFieldValidator = (
      control: FormControl
    ): { [s: string]: boolean } => {
      if (!control.value) {
        return { required: true };
      } else if (
        control.value !==
        this.contactInformationForm.get('password.newPassword').value
      ) {
        return { confirm: true, error: true };
      }
      return {};
    };

    return this.formBuilder.group({
      email: this.formBuilder.group({
        currentEmail: [{ value: signedUser.user.email, disabled: true }],
        newEmail: ['', [Validators.required, Validators.email]],
        confirmNewEmail: ['', [Validators.required, newEmailFieldValidator]],
      }),
      phoneNumber: this.formBuilder.group({
        currentPhoneNumber: [
          { value: signedUser.user.phoneNumber, disabled: true },
        ],
        newPhoneNumber: [
          '',
          [
            Validators.required,
            Validators.pattern(
              /^(\+\d{1,2}\s?)?1?\-?\.?\s?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}$/
            ),
          ],
        ],
        confirmNewPhoneNumber: [
          '',
          [
            Validators.required,
            Validators.pattern(
              /^(\+\d{1,2}\s?)?1?\-?\.?\s?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}$/
            ),
            newPhoneFieldValidator,
          ],
        ],
      }),
      password: this.formBuilder.group({
        currentPassword: ['', [Validators.required]],
        newPassword: ['', [Validators.required]],
        confirmNewPassword: [
          '',
          [Validators.required, newPasswordFieldValidator],
        ],
      }),
    });
  }

  onSubmitForm($event) {
    const contactInformation: ContactInformation = {
      email: null,
      phone_number: null,
      password: null,
    };

    if (this.updateEmail) {
      contactInformation.email = {
        current_email: this.contactInformationForm.get('email.currentEmail')
          .value,
        new_email: this.contactInformationForm.get('email.newEmail').value,
        confirm_email: this.contactInformationForm.get('email.confirmNewEmail')
          .value,
      };
    }

    if (this.updatePhoneNumber) {
      contactInformation.phone_number = {
        current_phone: this.contactInformationForm.get(
          'phoneNumber.currentPhoneNumber'
        ).value,
        new_phone: this.contactInformationForm.get('phoneNumber.newPhoneNumber')
          .value,
        confirm_phone: this.contactInformationForm.get(
          'phoneNumber.confirmNewPhoneNumber'
        ).value,
      };
    }

    if (this.updatePassword) {
      contactInformation.password = {
        old_password: this.contactInformationForm.get(
          'password.currentPassword'
        ).value,
        new_password: this.contactInformationForm.get('password.newPassword')
          .value,
        confirm_password: this.contactInformationForm.get(
          'password.confirmNewPassword'
        ).value,
      };
    }


    this.isLoading = true;
    this.identityService
      .updateContactInformation(contactInformation)
      .pipe(
        take(1),
        catchError((error) => {
          this.notification.create('error', 'Error', 'Something went wrong.', {
            nzPlacement: 'bottomRight',
          });
          return of(error);
        })
      )
      .subscribe((response) => {
        this.isLoading = false;
        this.notification.create(
          'success',
          'Success',
          'Your contact information has been successfully updated.',
          { nzPlacement: 'bottomRight' }
        );
        this.contactInformationForm.reset({});
        this.updateEmail = false;
        this.updatePhoneNumber = false;
        this.updatePassword = false;
      });
  }

  onUpdateEmailClick() {
    this.updateEmail = !this.updateEmail;
  }

  onUpdatePhoneNumberClick() {
    this.updatePhoneNumber = !this.updatePhoneNumber;
  }

  onUpdatePasswordClick() {
    this.updatePassword = !this.updatePassword;
  }

  updateConfirmNewEmailValidator(): void {
    /** wait for refresh value */
    Promise.resolve().then(() =>
      this.contactInformationForm
        .get('email.confirmNewEmail')
        .updateValueAndValidity()
    );
  }

  updateConfirmNewPhoneNumberValidator(): void {
    /** wait for refresh value */
    Promise.resolve().then(() =>
      this.contactInformationForm
        .get('phoneNumber.confirmNewPhoneNumber')
        .updateValueAndValidity()
    );
  }

  updateConfirmNewPasswordValidator(): void {
    /** wait for refresh value */
    Promise.resolve().then(() =>
      this.contactInformationForm
        .get('password.confirmNewPassword')
        .updateValueAndValidity()
    );
  }

  getDisabled(): boolean {
    let isDisabled = true;

    if (this.updateEmail) {
      if (this.contactInformationForm.controls.email.valid) {
        isDisabled = false;
      } else {
        return true;
      }
    }

    if (this.updatePhoneNumber) {
      if (this.contactInformationForm.controls.phoneNumber.valid) {
        isDisabled = false;
      } else {
        return true;
      }
    }

    if (this.updatePassword) {
      if (this.contactInformationForm.controls.password.valid) {
        isDisabled = false;
      } else {
        return true;
      }
    }

    return isDisabled;
  }

  // identityRevealedValidator: ValidatorFn = (control: AbstractControl): ValidationErrors | null => {
  //   const email = control.get('name');
  //   const  = control.get('alterEgo');

  //   return name && alterEgo && name.value === alterEgo.value ? { identityRevealed: true } : null;
  // };
}
