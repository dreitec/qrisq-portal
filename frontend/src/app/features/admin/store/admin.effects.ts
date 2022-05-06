import { HttpErrorResponse } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { Actions, createEffect, ofType } from '@ngrx/effects';
import { Store } from '@ngrx/store';
import { NzNotificationService } from 'ng-zorro-antd/notification';
import { EMPTY, of } from 'rxjs';
import { switchMap, map, catchError, take } from 'rxjs/operators';
import { GlobalConfigModel } from '../models/GlobalConfig.models';
import { QrAdminService } from '../services/admin.service';
import {
  actionAdminUserGetAllRequest,
  actionAdminUserGetAllRequestSucceeded,
  actionFetchGlobalConfigRequest,
  actionGlobalConfigRequestFailed,
  actionGlobalConfigRequestSuccess,
  actionUpdateGlobalConfigRequest,
  actionUpdateLoadingStatus,
} from './admin.actions';

@Injectable()
export class AdminEffects {
  /* -------------------------------------------------------------------------- */
  /*                             Check Service Area                             */
  /* -------------------------------------------------------------------------- */

  // request
  effectAdminUser = createEffect(
    () =>
      this.actions$.pipe(
        ofType(actionAdminUserGetAllRequest),
        switchMap((action) =>
          this.adminService.fetchUsers({}).pipe(
            map((data: any) => {
              return actionAdminUserGetAllRequestSucceeded({ data });
            }),
            catchError((error) => EMPTY)
          )
        )
      ),
    { dispatch: false }
  );

  /* -------------------------------------------------------------------------- */
  /*                          Settings / Global Config                          */
  /* -------------------------------------------------------------------------- */

  // fetch
  effectFetchGlobalConfigRequest = createEffect(() =>
    this.actions$.pipe(
      ofType(actionFetchGlobalConfigRequest),
      switchMap((action) =>
        this.adminService.fetchGlobalConfig().pipe(
          take(1),
          map((response: GlobalConfigModel) =>
            actionGlobalConfigRequestSuccess({ data: response })
          ),
          catchError((error: HttpErrorResponse) => {
            if (error.status === 400) {
              this.notification.create(
                'error',
                'Error',
                'Failed to load the globla config',
                { nzPlacement: 'bottomRight' }
              );
            } else {
              this.notification.create('error', 'Error', error.message, {
                nzPlacement: 'bottomRight',
              });
            }
            return of(actionGlobalConfigRequestFailed(error));
          })
        )
      )
    )
  );

  // update
  effectUpdateGlobalConfigRequest = createEffect(() =>
    this.actions$.pipe(
      ofType(actionUpdateGlobalConfigRequest),
      switchMap((action) =>
        this.adminService.updateGlobalConfig(action.data).pipe(
          take(1),
          map((response: GlobalConfigModel) => {
            this.notification.create(
              'success',
              'Success',
              'Successfully updated!',
              { nzPlacement: 'bottomRight' }
            );
            return actionGlobalConfigRequestSuccess({ data: response });
          }),
          catchError((error: HttpErrorResponse) => {
            if (error.status === 400) {
              this.notification.create(
                'error',
                'Error',
                'Failed to update the globla config',
                { nzPlacement: 'bottomRight' }
              );
            } else {
              this.notification.create('error', 'Error', error.message, {
                nzPlacement: 'bottomRight',
              });
            }
            return of(actionGlobalConfigRequestFailed(error));
          })
        )
      )
    )
  );

  constructor(
    private actions$: Actions,
    private adminService: QrAdminService,
    private router: Router,
    private route: ActivatedRoute,
    private store: Store,
    private notification: NzNotificationService
  ) {}
}
