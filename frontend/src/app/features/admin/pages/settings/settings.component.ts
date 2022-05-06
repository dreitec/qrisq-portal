import { Component } from '@angular/core';
import { Store } from '@ngrx/store';
import { GlobalConfigModel } from '../../models/GlobalConfig.models';
import { LoadingStatusModel } from '../../models/LoadingStatus.models';
import {
  actionFetchGlobalConfigRequest,
  actionUpdateGlobalConfigRequest,
  actionUpdateLoadingStatus,
} from '../../store/admin.actions';
import {
  selectGlobalConfig,
  selectLoadingStatus,
} from '../../store/admin.selectors';

@Component({
  selector: 'qr-admin-settings',
  templateUrl: './settings.component.html',
  styleUrls: ['./settings.component.scss'],
})
export class QrAdminSettingsComponent {
  constructor(private store: Store) {}

  isLoading = false;
  lookBackHrs = 0;
  overrideEnabled = false;
  activeStormEnabled = false;
  geocodeEnabled = false;

  globalConfig$ = this.store.select(selectGlobalConfig);
  loadingStatus$ = this.store.select(selectLoadingStatus);

  ngOnInit(): void {
    this.store.dispatch(actionFetchGlobalConfigRequest());

    this.globalConfig$.subscribe((data: GlobalConfigModel) => {
      this.lookBackHrs = data.lookback_period;
      this.overrideEnabled = data.lookback_override;
      this.activeStormEnabled = data.active_storm;
      this.geocodeEnabled = data.geocode_users;
    });
    this.loadingStatus$.subscribe((data: LoadingStatusModel) => {
      this.isLoading = data.globalConfig || false;
    });
  }

  onSave() {
    this.store.dispatch(actionUpdateLoadingStatus({ globalConfig: true }));
    this.store.dispatch(
      actionUpdateGlobalConfigRequest({
        data: {
          lookback_period: Number(this.lookBackHrs),
          lookback_override: this.overrideEnabled,
          active_storm: this.activeStormEnabled,
          geocode_users: this.geocodeEnabled,
        },
      })
    );
  }
}
