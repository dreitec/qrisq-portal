import { Component, OnInit } from '@angular/core';
import { Store } from '@ngrx/store';
import { map, take } from 'rxjs/operators';

import { SubscriptionPlan } from '../../models/SubscriptionPlan.model';
import { QrIdentityService } from '../../services/identity.service';
import { actionRegisterStart } from '../../store/identity.actions';
import { SignUpState } from '../../store/identity.models';
import { selectSignUp } from '../../store/identity.selectors';

@Component({
  selector: 'qr-service-area-available-page',
  templateUrl: './service-area-available.component.html',
  styleUrls: ['./service-area-available.component.scss'],
})
export class QrServiceAreaAvailablePageComponent implements OnInit {
  constructor(
    private identityService: QrIdentityService,
    private store: Store
  ) {}

  subscriptionPlans = [];

  signUp$ = this.store.select(selectSignUp);

  ngOnInit(): void {
    const myThis = this;
    this.signUp$.subscribe({
      next: (signUpData) =>
        signUpData &&
        myThis.fetchSubscriptionPlans(signUpData),
      error: (err) => console.error(err),
    });
  }

  fetchSubscriptionPlans(state: SignUpState): void {
    this.identityService
      .fetchSubscriptionPlansWithDiscount(state)
      .pipe(
        take(1),
        map((subscriptionPlans: SubscriptionPlan[]) => subscriptionPlans)
      )
      .subscribe((subscriptionPlans) => {
        this.subscriptionPlans = subscriptionPlans;
      });
  }

  public onRegister(planId: number): void {
    this.store.dispatch(actionRegisterStart({ subscriptionPlanId: planId }));
  }
}
