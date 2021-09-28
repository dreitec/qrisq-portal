import { Injectable } from '@angular/core';
import { Actions, createEffect, ofType } from '@ngrx/effects';
import { Store } from '@ngrx/store';
import { iif, of } from 'rxjs';
import { catchError, map, switchMap, take, tap } from 'rxjs/operators';
import { QrStormService } from '../services/storm.service';
import {
  actionStormDataFetchRequest,
  actionStormDataFetchRequestSuccess,
} from './storm.actions';
import { StorageMap } from '@ngx-pwa/local-storage';

import { selectStormData } from './storm.selectors';
import { StormData } from '../models/storm.models';

@Injectable()
export class QrStormEffects {
  constructor(
    private actions$: Actions,
    private stormService: QrStormService,
    private storage: StorageMap
  ) {}

  effectHurricaneDataFetchRequest = createEffect(() =>
    this.actions$.pipe(
      ofType(actionStormDataFetchRequest),
      switchMap((action) =>
        this.stormService.getStormData(action.freeMode).pipe(
          take(1),
          map((stormData) =>
            actionStormDataFetchRequestSuccess({
              stormData,
            })
          )
        )
      )
    )
  );
}

//   if(stormDataStore === null) {
//     return this.stormService
//       .getStormData(action.userId)
//       .pipe(
//         take(1),
//         map(stormDataResponse => actionStormDataFetchRequestSuccess({ stormData: stormDataResponse  }))
//       )
//     //                   .pipe(
//   }
//   return actionStormDataFetchRequestSuccess({ stormData: stormDataStore  });
// })));
// switchMap(stormData =>  ))
// actionStormDataFetchRequestSuccess({
//   stormData: iif(stormData === null,
//                 this.stormService.getStormData(action.userId)
//                   .pipe(
//                     switchMap(stormDataResponse => map(stormDataResponse => stormDataResponse))
//                     take(1), map(stormDataRes => stormDataRes)), stormData)) })))))
