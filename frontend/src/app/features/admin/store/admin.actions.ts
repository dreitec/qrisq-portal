import { HttpErrorResponse } from '@angular/common/http';
import { createAction, props } from '@ngrx/store';
import { AdminUser } from '../models/AdminUser.models';
import { GlobalConfigModel } from '../models/GlobalConfig.models';

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

/* -------------------------------------------------------------------------- */
/*                          Settings / Global Config                          */
/* -------------------------------------------------------------------------- */

// request
export const actionFetchGlobalConfigRequest = createAction(
  '[Settings] Fetch Global Config Request'
);

// success
export const actionFetchGlobalConfigRequestSuccess = createAction(
  '[Settings] Fetch Global Config Request Success',
  props<{
    data: GlobalConfigModel;
  }>()
);

// failed
export const actionFetchGlobalConfigRequestFailed = createAction(
  '[Settings] Fetch Global Config Request Failed',
  props<{ error: HttpErrorResponse }>()
);

// update request
export const actionUpdateGlobalConfigRequest = createAction(
  '[Settings] Update Global Config Request',
  props<{
    data: GlobalConfigModel;
  }>()
);

// update success
export const actionUpdateGlobalConfigRequestSuccess = createAction(
  '[Settings] Update Global Config Request Success',
  props<{
    data: GlobalConfigModel;
  }>()
);

// update failed
export const actionUpdateGlobalConfigRequestFailed = createAction(
  '[Settings] Update Global Config Request Failed',
  props<{ error: HttpErrorResponse }>()
);
