import { Injectable } from '@angular/core';
import { ComponentStore } from '@ngrx/component-store';
import { Observable } from 'rxjs';

export interface QrCheckServiceAreaState {
  lattitude: number | null;
  longitude: number | null;
}

export const DEFAULT_STATE: QrCheckServiceAreaState = {
  lattitude: null,
  longitude: null,
};

@Injectable()
export class QrCheckServiceAreaComponentStore extends ComponentStore<QrCheckServiceAreaState> {
  constructor() {
    super(DEFAULT_STATE);
  }

  readonly location$: Observable<{
    lattitude: number | null;
    longitude: number | null;
  }> = this.select((state) => ({
    lattitude: state.lattitude,
    longitude: state.longitude,
  }));

  // selectors
  readonly IsLocation$: Observable<boolean> = this.select(
    (state) => state.lattitude !== null && state.longitude !== null
  );

  // updaters
  readonly updateLocation = this.updater(
    (
      state: QrCheckServiceAreaState,
      location: { lattitude: number; longitude: number }
    ) => {
      return {
        ...state,
        lattitude: location.lattitude,
        longitude: location.longitude,
      };
    }
  );

  resetState(): void {
    this.setState(DEFAULT_STATE);
  }
}
