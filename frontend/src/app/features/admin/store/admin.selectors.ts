// ngrx
import { RootState } from '@app/core/store/state';
import { createFeatureSelector, createSelector } from '@ngrx/store';
import { AdminState } from './admin.state';

export const selectAdminState = createFeatureSelector<RootState, AdminState>(
  'admin'
);

// global config
export const selectGlobalConfig = createSelector(
  selectAdminState,
  (state: AdminState) => state.globalConfig
);

// loading status
export const selectLoadingStatus = createSelector(
  selectAdminState,
  (state: AdminState) => state.loading
);
