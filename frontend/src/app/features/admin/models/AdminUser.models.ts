export interface AdminUser {
  id: number;
  email: string;
  firstName: string;
  lastName: string;
  isAdmin: boolean;
}

export interface AdminUserTableDataItem {
  id: number;
  email: string;
  firstName: string;
  lastName: string;
  isAdmin: boolean;
}

export interface AdminUserTableData {
  data: AdminUserTableDataItem[];
  totalRecords: number;
  totalPages: number;
}

export interface AdminUserHttpGetResponseModel {
  id: number;
  email: string;
  first_name: string;
  last_name: string;
  is_admin: boolean;
}

export interface AdminUsersHttpGetResponseModel {
  links: any;
  results: Array<{
    id: number;
    email: string;
    first_name: string;
    last_name: string;
    is_admin: boolean;
  }>;
  total_pages: number;
  total_records: number;
}

export interface AdminBillingData {
  results: AdminBillingItem[];
  totalRecords: number;
  totalPages: number;
}

export interface AdminBillingItem {
  id: number;
  type: string;
  name: string;
  startDate: string;
  endDate: string;
  status: number;
  discount: number;
  users: number;
}
