import { HttpErrorResponse } from '@angular/common/http';
import { StormData } from '../models/storm.models';

export interface StormState {
  stormData: StormData;
  errors: Array<HttpErrorResponse>;
  loading: boolean;
}

export const initialState: StormState = {
  stormData: null,
  errors: [],
  loading: false,
};
