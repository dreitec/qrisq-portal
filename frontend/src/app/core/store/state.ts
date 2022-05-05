import {
  ActionReducer,
  ActionReducerMap,
  createFeatureSelector,
} from '@ngrx/store';
import { routerReducer, RouterReducerState } from '@ngrx/router-store';
import { Params } from '@angular/router';
import { storageSync } from '@larscom/ngrx-store-storagesync';

import { AdminReducer } from '@app/features/admin/store/admin.reducers';
import { AdminState } from '@app/features/admin/store/admin.state';
import { IdentityReducer } from '@app/features/identity/store/identity.reducer';
import { IdentityState } from '@app/features/identity/store/identity.models';
import { StormReducer } from '@app/features/storm/store/storm.reducer';
import { StormState } from '@app/features/storm/store/storm.state';


export function storageSyncReducer(reducer: ActionReducer<RootState>) {
  const metaReducer = storageSync<RootState>({
    version: 1,
    features: [
      {
        stateKey: 'identity',
      },
    ],
    storage: window.localStorage,
    storageError: console.error,
    rehydrate: true,
  });

  return metaReducer(reducer);
}

export const reducers: ActionReducerMap<RootState> = {
  admin: AdminReducer,
  identity: IdentityReducer,
  storm: StormReducer,
  router: routerReducer,
};

export interface RouterStateUrl {
  url: string;
  params: Params;
  queryParams: Params;
}

export interface RootState {
  admin: AdminState;
  identity: IdentityState;
  storm: StormState;
  router: RouterReducerState<RouterStateUrl>;
}
