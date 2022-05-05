// ngrx
import { RootState } from '@app/core/store/state';
import { createFeatureSelector, createSelector } from '@ngrx/store';
import { AdminState } from './admin.state';

export const selectAdminState = createFeatureSelector<
  RootState,
  AdminState
>('admin');

// signUp
export const selectGlobalConfig = createSelector(
  selectAdminState,
  (state: AdminState) => state.globalConfig
);
