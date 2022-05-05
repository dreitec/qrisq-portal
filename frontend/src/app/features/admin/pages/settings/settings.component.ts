import { Component } from '@angular/core';
import { Store } from '@ngrx/store';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';
import { GlobalConfigModel } from '../../models/GlobalConfig.models';
import { actionFetchGlobalConfigRequest, actionUpdateGlobalConfigRequest } from '../../store/admin.actions';
import { selectGlobalConfig } from '../../store/admin.selectors';

@Component({
  selector: 'qr-admin-settings',
  templateUrl: './settings.component.html',
  styleUrls: ['./settings.component.scss'],
})
export class QrAdminSettingsComponent {

  constructor(
    private store: Store
  ) {}

  isLoading = false;
  lookBackHrs = 0;
  overrideEnabled = false;
  activeStormEnabled = false;
  geocodeEnabled = false;

  globalConfig$ = this.store.select(selectGlobalConfig);

  ngOnInit(): void {
    this.store.dispatch(actionFetchGlobalConfigRequest());

    this.globalConfig$.subscribe((data: GlobalConfigModel) => {
      this.lookBackHrs = data.lookback_period;
      this.overrideEnabled = data.lookback_override;
      this.activeStormEnabled = data.active_storm;
    });
  }

  onBlur() {
    console.log('Look Back hrs: ', this.lookBackHrs);
  }

  onSave() {
    this.store.dispatch(actionUpdateGlobalConfigRequest({
      data: {
        lookback_period: Number(this.lookBackHrs),
        lookback_override: this.overrideEnabled,
        active_storm: this.activeStormEnabled
      }
    }));
  }
}
