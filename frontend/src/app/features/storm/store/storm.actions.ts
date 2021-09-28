import { createAction, props } from '@ngrx/store';
import { StormData } from '../models/storm.models';

/* -------------------------------------------------------------------------- */
/*                              Storm Data Fetch                              */
/* -------------------------------------------------------------------------- */

export const actionStormDataFetchRequest = createAction(
  '[Storm] Storm Data Fetch Request',
  props<{ freeMode: boolean }>()
);

export const actionStormDataFetchRequestSuccess = createAction(
  '[Storm] Storm Data Fetch Request Success',
  props<{ stormData: StormData }>()
);

export const actionStormDataFetchRequestFailed = createAction(
  '[Storm] Storm Data Fetch Request Failed'
);
