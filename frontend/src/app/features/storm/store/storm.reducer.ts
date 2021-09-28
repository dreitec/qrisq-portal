import { Action, createReducer, on } from '@ngrx/store';
import {
  actionStormDataFetchRequestFailed,
  actionStormDataFetchRequest,
  actionStormDataFetchRequestSuccess,
} from './storm.actions';
import { StormState, initialState } from './storm.state';

const reducer = createReducer(
  initialState,

  /* -------------------------------------------------------------------------- */
  /*                           Action Storm Data Fetch                          */
  /* -------------------------------------------------------------------------- */

  // request
  on(actionStormDataFetchRequest, (state) => ({
    ...state,
    loading: true,
  })),

  // success
  on(actionStormDataFetchRequestSuccess, (state, { stormData }) => ({
    ...state,
    stormData,
    loading: false,
  })),

  // failed
  on(actionStormDataFetchRequestFailed, (state) => ({
    ...state,
    loading: false,
  }))
);

export function StormReducer(
  state: StormState | undefined,
  action: Action
): StormState {
  return reducer(state, action);
}
