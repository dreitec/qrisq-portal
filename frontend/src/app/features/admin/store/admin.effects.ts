import { Injectable } from "@angular/core";
import { ActivatedRoute, Router } from "@angular/router";
import { Actions, createEffect, ofType } from "@ngrx/effects";
import { Store } from "@ngrx/store";
import { NzNotificationService } from "ng-zorro-antd/notification";
import { EMPTY } from "rxjs";
import { switchMap, map, catchError } from "rxjs/operators";
import { QrAdminService } from "../services/admin.service";
import { actionAdminUserGetAllRequest, actionAdminUserGetAllRequestSucceeded } from "./admin.actions";

@Injectable()
export class AdminEffects {

  constructor(
    private actions$: Actions,
    private admninService: QrAdminService,
    private router: Router,
    private route: ActivatedRoute,
    private store: Store,
    private notification: NzNotificationService,
  ) {}

  /* -------------------------------------------------------------------------- */
  /*                             Check Service Area                             */
  /* -------------------------------------------------------------------------- */

  // request
  effectAdminUser = createEffect(() =>
  this.actions$.pipe(
    ofType(actionAdminUserGetAllRequest),
    switchMap((action) =>
      this.adminService
        .pipe(            
          map((data: AdminUserGetAllResponse) => {
            return actionAdminUserGetAllRequestSucceeded({ data })
          })
          catchError((error) => EMPTY)
        )
    )
  ) 
  );

}

            }