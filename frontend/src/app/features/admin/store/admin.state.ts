import { HttpRequestStatus } from '@app/shared/enums/HttpRequestStatus.enum';
import { AdminUser } from '../models/AdminUser.models';
import { ClientUser } from '../models/ClientUser.models';
import { AdminUserGetAllResponse } from './admin.';

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
};
