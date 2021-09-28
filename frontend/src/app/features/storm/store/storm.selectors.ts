import { RootState } from '@app/core/store/state';
import { createFeatureSelector, createSelector } from '@ngrx/store';
import { StormState } from './storm.state';

export const selectStormState = createFeatureSelector<RootState, StormState>(
  'storm'
);

export const selectStormData = createSelector(
  selectStormState,
  (state: StormState) => state.stormData
);
