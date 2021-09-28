export interface SubscriptionPlansHttpGetResponseModel {
  links: any;
  results: Array<{
    id: number;
    name: string;
    feature: string;
    price: number;
    duration: number;
  }>;
  total_pages: number;
  total_records: number;
}

export interface SubscriptionPlanHttpGetResponseModel {
  id: number;
  name: string;
  feature: string;
  price: number;
  duration: number;
}

export interface SubscriptionPlanTableData {
  data: SubscriptionPlanTableDataItem[];
  totalRecords: number;
  totalPages: number;
}

export interface SubscriptionPlanTableDataItem {
  id: number;
  name: string;
  price: number;
  duration: number;
}
