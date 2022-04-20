// angular
import { Component, OnInit } from '@angular/core';

// store
import { Store } from '@ngrx/store';
import { actionRegisterStart } from '../../store/identity.actions';

import { QrIdentityService } from '../../services/identity.service';
import { selectSignUp } from '../../store/identity.selectors';
import { Observable } from 'rxjs';
import { map, take, tap } from 'rxjs/operators';
import { SubscriptionPlan } from '../../models/SubscriptionPlan.model';

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

  myState = ''
  subscriptionPlans = []

  signUp$ = this.store.select(selectSignUp);

  ngOnInit(): void {
    this.signUp$
      .pipe(
        take(1),
        map((signUpData) => signUpData)
      )
      .subscribe((signUpData) => {
        this.myState = signUpData.addressState || '';
      });

    this.identityService.fetchSubscriptionPlansWithDiscount(this.myState).pipe(
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