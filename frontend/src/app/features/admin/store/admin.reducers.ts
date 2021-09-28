import { HttpRequestStatus } from './../../../shared/enums/HttpRequestStatus.enum';
import { Action, createReducer, on } from '@ngrx/store';
import { AdminState, initialState } from './admin.state';
import { actionAdminUsersGetAllRequest } from './admin.actions';

const reducer = createReducer(
  initialState,
  on(actionAdminUsersGetAllRequest, (state) => ({
    ...state,
    adminUser: {
      data: [],
      request: {
        status: HttpRequestStatus.REQUESTED,
        error: '',
      },
    },
  }))
);

export function AdminReducer(
  state: AdminState | undefined,
  action: Action
): AdminState {
  return reducer(state, action);
}
