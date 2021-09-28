import { HttpErrorResponse } from '@angular/common/http';
import { createAction, props } from '@ngrx/store';
import { AdminUser } from '../models/AdminUser.models';

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
