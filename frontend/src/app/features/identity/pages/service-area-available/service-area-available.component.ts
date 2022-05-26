import { Component, OnInit } from '@angular/core';
import { Store } from '@ngrx/store';
import { BehaviorSubject, Observable, of } from 'rxjs';
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

  isFetching = false;
  isLoading = false;

  signUp$ = this.store.select(selectSignUp);
  subscriptionPlans$ = new Observable<SubscriptionPlan[]>();

  ngOnInit(): void {
    this.isLoading = true;
    this.signUp$.subscribe({
      next: (signUpData) =>
        signUpData.addressCity && signUpData.addressState &&
        !this.isFetching && this.fetchSubscriptionPlans(signUpData),
      error: (err) => console.error(err),
    });
  }

  fetchSubscriptionPlans(state: SignUpState): void {
    this.isFetching = true;
    this.identityService
      .fetchSubscriptionPlansWithDiscount(state)
      .pipe(
        take(1),
        map((plans: SubscriptionPlan[]) => plans)
      )
      .subscribe((plans) => {
        this.subscriptionPlans$ = of(plans);
        this.isLoading = false;
      });
  }

  public onRegister(planId: number): void {
    this.store.dispatch(actionRegisterStart({ subscriptionPlanId: planId }));
  }
}
