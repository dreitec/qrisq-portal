import { HttpRequestStatus } from '@app/shared/enums/HttpRequestStatus.enum';
import { AdminUser } from '../models/AdminUser.models';
import { ClientUser } from '../models/ClientUser.models';
import { GlobalConfigModel } from '../models/GlobalConfig.models';
import { LoadingStatusModel } from '../models/LoadingStatus.models';

export interface AdminState {
  adminUser: {
    data: AdminUser[];
    request: {
      status: HttpRequestStatus;
      error: string;
    };
  };
  clientUser: {
    data: ClientUser[];
    request: {
      status: HttpRequestStatus;
      error: string;
    };
  };
  globalConfig: GlobalConfigModel;
  loading: LoadingStatusModel;
}

export const initialState: AdminState = {
  adminUser: {
    data: [],
    request: { status: HttpRequestStatus.NONE, error: '' },
  },
  clientUser: {
    data: [],
    request: { status: HttpRequestStatus.NONE, error: '' },
  },
  globalConfig: {
    lookback_period: 0,
    lookback_override: false,
    active_storm: false,
    geocode_users: false,
  },
  loading: {
    globalConfig: false,
  },
};
