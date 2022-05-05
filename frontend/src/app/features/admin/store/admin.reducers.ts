import { HttpRequestStatus } from './../../../shared/enums/HttpRequestStatus.enum';
import { Action, createReducer, on } from '@ngrx/store';
import { AdminState, initialState } from './admin.state';
import { actionAdminUserGetAllRequest, actionFetchGlobalConfigRequestSuccess } from './admin.actions';

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
  on(actionFetchGlobalConfigRequestSuccess, (state, { data }) => ({
    ...state,
    globalConfig: data,
  }))
);

export function AdminReducer(
  state: AdminState | undefined,
  action: Action
): AdminState {
  return reducer(state, action);
}
