import { HttpErrorResponse } from '@angular/common/http';
import { createAction, props } from '@ngrx/store';
import { AdminUser } from '../models/AdminUser.models';
import { GlobalConfigModel } from '../models/GlobalConfig.models';
import { LoadingStatusModel } from '../models/LoadingStatus.models';

// request

export const actionAdminUserGetAllRequest = createAction(
  '[Admin] Admin User Get All Request'
);

// success

export const actionAdminUserGetAllRequestSucceeded = createAction(
  '[Admin] Admin User Get All Request Succeeded',
  props<{ data: AdminUser[] }>()
);

// failed

export const actionAdminUserGetAllRequestFailed = createAction(
  '[Admin] Admin User Get All Request Failed',
  props<{ error: HttpErrorResponse }>()
);

// update `loading` status
export const actionUpdateLoadingStatus = createAction(
  '[Admin] Update Loading Status',
  props<LoadingStatusModel>()
);

/* -------------------------------------------------------------------------- */
/*                          Settings / Global Config                          */
/* -------------------------------------------------------------------------- */

// fetch request
export const actionFetchGlobalConfigRequest = createAction(
  '[Settings] Fetch Global Config Request'
);

// update request
export const actionUpdateGlobalConfigRequest = createAction(
  '[Settings] Update Global Config Request',
  props<{
    data: GlobalConfigModel;
  }>()
);

// request success
export const actionGlobalConfigRequestSuccess = createAction(
  '[Settings] Global Config Request Success',
  props<{
    data: GlobalConfigModel;
  }>()
);

// request failed
export const actionGlobalConfigRequestFailed = createAction(
  '[Settings] Global Config Request Failed',
  props<{ error: HttpErrorResponse }>()
);
