import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Store } from '@ngrx/store';
import { NzNotificationService } from 'ng-zorro-antd/notification';
import { take } from 'rxjs/operators';
import { QrIdentityService } from '../../services/identity.service';
import { actionSignOut } from '../../store/identity.actions';

@Component({
  selector: 'qr-cancel-subscription-page',
  templateUrl: './cancel-subscription.component.html',
  styleUrls: ['./cancel-subscription.component.scss'],
})
export class QrCancelSubscriptionPageComponent implements OnInit {
  isLoading = false;

  cancelSubscriptionForm: FormGroup;

  constructor(
    private formBuilder: FormBuilder,
    private identityService: QrIdentityService,
    private notification: NzNotificationService,
    private store: Store
  ) {}

  ngOnInit() {
    this.cancelSubscriptionForm = this.formBuilder.group({
      message: ['', [Validators.required]],
    });
  }

  onSubmitForm($event) {
    const message = this.cancelSubscriptionForm.get('message').value;
    this.isLoading = true;
    this.identityService
      .cancelSubscription()
      .pipe(take(1))
      .subscribe(
        (response) => {
          this.isLoading = false;
          this.notification.create(
            'success',
            'Success',
            'Your subscription was successfully cancelled.',
            { nzPlacement: 'bottomRight' }
          );
          this.store.dispatch(actionSignOut({ refreshToken: 'token' }));
        },
        (error) => {
          this.isLoading = false;
          this.notification.create('error', 'Error', 'Something went wrong.');
        }
      );
  }
}
