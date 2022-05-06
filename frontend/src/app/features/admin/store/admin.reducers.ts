import { HttpRequestStatus } from './../../../shared/enums/HttpRequestStatus.enum';
import { Action, createReducer, on } from '@ngrx/store';
import { AdminState, initialState } from './admin.state';
import {
  actionAdminUserGetAllRequest,
  actionGlobalConfigRequestFailed,
  actionGlobalConfigRequestSuccess,
  actionUpdateLoadingStatus,
} from './admin.actions';

const reducer = createReducer(
  initialState,
  on(actionAdminUserGetAllRequest, (state) => ({
    ...state,
    adminUser: {
      data: [],
      request: {
        status: HttpRequestStatus.REQUESTED,
        error: '',
      },
    },
  })),
  on(actionGlobalConfigRequestSuccess, (state, { data }) => ({
    ...state,
    globalConfig: data,
    loading: {
      ...state.loading,
      globalConfig: false,
    },
  })),
  on(actionGlobalConfigRequestFailed, (state, data) => ({
    ...state,
    loading: {
      ...state.loading,
      globalConfig: false,
    },
  })),
  on(actionUpdateLoadingStatus, (state, data) => ({
    ...state,
    loading: {
      ...state.loading,
      ...data,
    },
  }))
);

export function AdminReducer(
  state: AdminState | undefined,
  action: Action
): AdminState {
  return reducer(state, action);
}
