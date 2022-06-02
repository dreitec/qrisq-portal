import {
  SubscriptionPlanTableData,
  SubscriptionPlanTableDataItem,
} from './../../models/SubscriptionPlan.model';
import { QrAdminService } from './../../services/admin.service';
import {
  AdminUserTableData,
  AdminUserTableDataItem,
} from './../../models/AdminUser.models';
import { Component, Inject, OnInit } from '@angular/core';
import {
  ClientUserTableData,
  ClientUserTableDataItem,
} from '../../models/ClientUser.models';
import { catchError, map, take } from 'rxjs/operators';
import { Observable, of } from 'rxjs';
import { NzTableQueryParams } from 'ng-zorro-antd/table';
import {
  FormBuilder,
  FormControl,
  FormGroup,
  Validators,
} from '@angular/forms';
import { NzNotificationService } from 'ng-zorro-antd/notification';
import { PageScrollService } from 'ngx-page-scroll-core';
import { DOCUMENT } from '@angular/common';

@Component({
  selector: 'qr-admin-panel-page',
  templateUrl: './admin-panel.component.html',
  styleUrls: ['./admin-panel.component.scss'],
})
export class QrAdminPanelPageComponent implements OnInit {
  selectedTable: string;
  selectedAction: string;
  selectedTableItemId: number;
  selectedTableItemData: any;

  tableRecordCount: number;
  tablePageSize: number;
  tablePageIndex: number;

  adminUsers: AdminUserTableData;
  adminUsers$: Observable<AdminUserTableData>;

  clientUsers: ClientUserTableData;
  clientUsers$: Observable<ClientUserTableData>;

  subscriptionPlans: SubscriptionPlanTableData;
  subscriptionPlans$: Observable<SubscriptionPlanTableData>;

  passwordFieldValidator = (control: FormControl): { [s: string]: boolean } => {
    if (!control.value) {
      return { required: true };
    } else if (
      control.value !== this.adminUserInsertForm.controls.password.value
    ) {
      return { confirm: true, error: true };
    }
    return {};
  };

  adminUserInsertForm: FormGroup = this.formBuilder.group({
    firstName: ['', [Validators.required]],
    lastName: ['', [Validators.required]],
    email: ['', [Validators.required, Validators.email]],
    phoneNumber: ['', [Validators.required]],
    streetNumber: ['', [Validators.required]],
    city: ['', [Validators.required]],
    state: ['', [Validators.required]],
    zipCode: ['', [Validators.required]],
    isAdmin: [true],
    password: [null, [Validators.required, Validators.minLength(12)]],
    checkPassword: [null, [Validators.required, this.passwordFieldValidator]],
  });

  clientUserUpdateForm: FormGroup = this.formBuilder.group({
    firstName: ['', [Validators.required]],
    lastName: ['', [Validators.required]],
    email: ['', [Validators.required, Validators.email]],
    phoneNumber: ['', [Validators.required]],
    streetNumber: ['', [Validators.required]],
    city: ['', [Validators.required]],
    state: ['', [Validators.required]],
    zipCode: ['', [Validators.required]],
  });

  clientUserSearchForm: FormGroup = this.formBuilder.group({
    firstName: ['', []],
    lastName: ['', []],
    email: ['', []],
  });

  subscriptionPlanSearchForm: FormGroup = this.formBuilder.group({
    name: ['', []],
    price: ['', []],
  });

  subscriptionPlanInsertForm: FormGroup = this.formBuilder.group({
    name: ['', [Validators.required]],
    price: ['', [Validators.required]],
    duration: ['', [Validators.required]],
    fluidpay_plan_id: ['', [Validators.required]],
  });

  subscriptionPlanUpdateForm: FormGroup = this.formBuilder.group({
    name: ['', [Validators.required]],
    price: ['', [Validators.required]],
    duration: ['', [Validators.required]],
    fluidpay_plan_id: ['', [Validators.required]],
  });

  loading: boolean;
  isActionLoading: boolean;

  constructor(
    private adminService: QrAdminService,
    private formBuilder: FormBuilder,
    private notification: NzNotificationService,
    private pageScrollService: PageScrollService,
    @Inject(DOCUMENT) private document: any
  ) {}

  ngOnInit() {
    this.loading = false;
    this.tableRecordCount = 0;
    this.selectedTable = '';
    this.selectedTableItemId = 0;
    this.selectedTableItemData = null;

    // adminUsers
    this.adminUsers = {
      data: [],
      totalRecords: 0,
      totalPages: 0,
    };

    // clientUsers
    this.clientUsers = {
      data: [],
      totalRecords: 0,
      totalPages: 0,
    };

    // subscriptionPlans
    this.subscriptionPlans = {
      data: [],
      totalRecords: 0,
      totalPages: 0,
    };
  }

  onTableSelected(selectedTable) {
    this.selectedTable = selectedTable;
    this.loading = true;
    switch (this.selectedTable) {
      case 'admin':
        this.adminUsers$ = this.fetchAdminUsers({ page: 1 });
        this.adminUsers$.subscribe((adminUsers) => {
          this.adminUsers = adminUsers;
          this.tableRecordCount = adminUsers.totalRecords;
          this.tablePageSize = 25;
          this.tablePageIndex = 1;
          this.loading = false;
        });
        break;
      case 'users':
        this.clientUsers$ = this.fetchClientUsers({ page: 1 });
        this.clientUsers$.subscribe((clientUsers) => {
          this.clientUsers = clientUsers;
          this.tableRecordCount = clientUsers.totalRecords;
          this.tablePageSize = 25;
          this.tablePageIndex = 1;
          this.loading = false;
        });
        break;
      case 'subscriptions':
        this.subscriptionPlans$ = this.fetchSubscriptionPlans({ page: 1 });
        this.subscriptionPlans$.subscribe((subscriptionPlans) => {
          this.subscriptionPlans = subscriptionPlans;
          this.tableRecordCount = subscriptionPlans.totalRecords;
          this.tablePageSize = 25;
          this.tablePageIndex = 1;
          this.loading = false;
        });
        break;

      default:
        break;
    }
  }

  onTableItemChecked(id: number, checked: boolean) {
    if (checked) {
      this.selectedTableItemId = id;
    } else {
      this.selectedTableItemId = 0;
    }
  }

  fetchSubscriptionPlans(params) {
    return this.adminService.fetchSubscriptionPlans(params).pipe(
      take(1),
      map((response) => {
        const subscriptionPlanTableData: SubscriptionPlanTableData = {
          data: response.results.map((item: any) => {
            const subscriptionPlanTableItem: SubscriptionPlanTableDataItem = {
              id: item.id,
              name: item.name,
              duration: item.duration,
              price: item.price,
              fluidpay_plan_id: item.fluidpay_plan_id,
            };
            return subscriptionPlanTableItem;
          }),
          totalPages: response.total_pages,
          totalRecords: response.total_records,
        };
        return subscriptionPlanTableData;
      })
    );
  }

  fetchAdminUsers(params) {
    return this.adminService.fetchAdmins(params).pipe(
      take(1),
      map((response) => {
        const adminUserTableData: AdminUserTableData = {
          data: response.results.map((item) => {
            const adminUserTableItem: AdminUserTableDataItem = {
              id: item.id,
              firstName: item.first_name,
              lastName: item.last_name,
              email: item.email,
              isAdmin: item.is_admin,
            };
            return adminUserTableItem;
          }),
          totalPages: response.total_pages,
          totalRecords: response.total_records,
        };
        return adminUserTableData;
      })
    );
  }

  onQueryParamsChange(params: NzTableQueryParams) {
    const { pageIndex } = params;
    if (pageIndex && pageIndex !== this.tablePageIndex) {
      switch (this.selectedTable) {
        case 'admin':
          this.loading = true;
          this.adminUsers$ = this.fetchAdminUsers({ page: pageIndex });
          this.adminUsers$.subscribe((adminUsers) => {
            this.adminUsers = adminUsers;
            this.tableRecordCount = adminUsers.totalRecords;
            this.tablePageSize = 25;
            this.tablePageIndex = pageIndex;
            this.loading = false;
          });
          break;
        case 'users':
          this.loading = true;
          this.clientUsers$ = this.fetchClientUsers({ page: pageIndex });
          this.clientUsers$.subscribe((clientUsers) => {
            this.clientUsers = clientUsers;
            this.tableRecordCount = clientUsers.totalRecords;
            this.tablePageSize = 25;
            this.tablePageIndex = pageIndex;
            this.loading = false;
          });
          break;
        case 'subscriptions':
          this.loading = true;
          this.subscriptionPlans$ = this.fetchSubscriptionPlans({
            page: pageIndex,
          });
          this.subscriptionPlans$.subscribe((subscriptionPlans) => {
            this.subscriptionPlans = subscriptionPlans;
            this.tableRecordCount = subscriptionPlans.totalRecords;
            this.tablePageSize = 25;
            this.tablePageIndex = pageIndex;
            this.loading = false;
          });
          break;

        default:
          break;
      }
    }
  }

  updatePasswordConfirmValidator(): void {
    /** wait for refresh value */
    Promise.resolve().then(() =>
      this.adminUserInsertForm.controls.checkPassword.updateValueAndValidity()
    );
  }

  onSubscriptionPlanInsertClick(event) {
    this.selectedAction = 'insert';
    this.pageScrollService.scroll({
      document: this.document,
      scrollTarget: '.table-data',
    });
  }

  onSubscriptionPlanUpdateClick(event) {
    this.isActionLoading = true;
    this.selectedAction = 'update';
    this.pageScrollService.scroll({
      document: this.document,
      scrollTarget: '.table-data',
    });
    this.adminService
      .fetchSubscriptionPlan(this.selectedTableItemId)
      .subscribe((response) => {
        this.selectedTableItemData = response;
        const formValue = {
          name: response.name,
          price: response.price,
          duration: response.duration,
          fluidpay_plan_id: response.fluidpay_plan_id,
        };
        this.subscriptionPlanUpdateForm.setValue(formValue);
        this.isActionLoading = false;
      });
  }

  onSubscriptionPlanSearchClick(event) {
    this.selectedAction = 'search';
    this.pageScrollService.scroll({
      document: this.document,
      scrollTarget: '.table-data',
    });
  }

  onSubscriptionPlanSearchCancelForm(event) {
    this.subscriptionPlanSearchForm.reset({});
    this.selectedAction = '';
  }

  onSubscriptionPlanInsertSubmitForm(event) {
    for (const i in this.subscriptionPlanInsertForm.controls) {
      this.subscriptionPlanInsertForm.controls[i].markAsDirty();
      this.subscriptionPlanInsertForm.controls[i].updateValueAndValidity();
    }
    this.isActionLoading = true;

    const { name, price, duration } = this.subscriptionPlanInsertForm.value;

    const params = {
      name,
      price,
      duration,
    };

    this.adminService
      .insertSubscriptionPlan(params)
      .pipe(
        take(1),
        catchError((error) => {
          this.notification.create('error', 'Error', 'Something went wrong.');
          return of(error);
        })
      )
      .subscribe((response) => {
        this.isActionLoading = false;
        this.notification.create(
          'success',
          'Success',
          'Subscription Plan added successfully!.',
          { nzPlacement: 'bottomRight' }
        );
        this.subscriptionPlanInsertForm.reset({});
        this.loading = true;
        this.selectedAction = '';
        this.subscriptionPlans$ = this.fetchSubscriptionPlans({ page: 1 });
        this.subscriptionPlans$.subscribe((subscriptionPlans) => {
          this.subscriptionPlans = subscriptionPlans;
          this.tableRecordCount = subscriptionPlans.totalRecords;
          this.loading = false;
        });
      });
  }

  onSubscriptionPlanInsertCancelForm(event) {
    this.subscriptionPlanInsertForm.reset({});
    this.selectedAction = '';
  }

  onSubscriptionPlanUpdateSubmitForm(event) {
    for (const i in this.subscriptionPlanUpdateForm.controls) {
      this.subscriptionPlanUpdateForm.controls[i].markAsDirty();
      this.subscriptionPlanUpdateForm.controls[i].updateValueAndValidity();
    }

    this.isActionLoading = true;

    const subscriptionPlanId = this.selectedTableItemId;
    const subscriptionPlanData = this.selectedTableItemData;

    const { name, price, duration, fluidpay_plan_id } = this.subscriptionPlanUpdateForm.value;

    const params = {
      name,
      price,
      duration,
      feature: subscriptionPlanData.feature,
      fluidpay_plan_id,
    };

    this.adminService
      .updateSubscriptionPlan(subscriptionPlanId, params)
      .pipe(
        take(1),
        catchError((error) => {
          this.notification.create('error', 'Error', 'Something went wrong.');
          return of(error);
        })
      )
      .subscribe((response) => {
        this.isActionLoading = false;
        this.notification.create(
          'success',
          'Success',
          'Data updated successfully!.',
          { nzPlacement: 'bottomRight' }
        );
        this.subscriptionPlanUpdateForm.reset({});
        this.loading = true;
        this.selectedAction = '';
        this.selectedTableItemId = 0;
        this.selectedTableItemData = null;
        this.subscriptionPlans$ = this.fetchSubscriptionPlans({
          page: this.tablePageIndex,
        });
        this.subscriptionPlans$.subscribe((subscriptionPlans) => {
          this.subscriptionPlans = subscriptionPlans;
          this.loading = false;
        });
      });
  }

  onSubscriptionPlanDeleteConfirm() {
    this.loading = true;

    const subscriptionPlanId = this.selectedTableItemId;
    this.adminService
      .deleteSubscriptionPlan(subscriptionPlanId)
      .pipe(
        take(1),
        catchError((error) => {
          this.notification.create('error', 'Error', 'Something went wrong.');
          return of(error);
        })
      )
      .subscribe((response) => {
        this.loading = false;
        this.notification.create(
          'success',
          'Success',
          'Subscription Plan deleted successfully!.',
          { nzPlacement: 'bottomRight' }
        );
        this.subscriptionPlans$ = this.fetchSubscriptionPlans({
          page: this.tablePageIndex,
        });
        this.subscriptionPlans$.subscribe((subscriptionPlans) => {
          this.subscriptionPlans = subscriptionPlans;
          this.tableRecordCount = subscriptionPlans.totalRecords;
          this.loading = false;
        });
      });
  }

  onSubscriptionPlanUpdateCancelForm(event) {
    this.subscriptionPlanUpdateForm.reset({});
    this.selectedAction = '';
    this.selectedTableItemData = null;
  }

  onSubscriptionPlanSearchSubmitForm(event) {
    for (const i in this.subscriptionPlanSearchForm.controls) {
      this.subscriptionPlanSearchForm.controls[i].markAsDirty();
      this.subscriptionPlanSearchForm.controls[i].updateValueAndValidity();
    }

    this.isActionLoading = true;

    const { name, price } = this.subscriptionPlanSearchForm.value;

    const params = {
      name,
      price,
    };

    this.subscriptionPlans$ = this.fetchSubscriptionPlans(params);
    this.subscriptionPlans$.subscribe((subscriptionPlans) => {
      this.subscriptionPlans = subscriptionPlans;
      this.tableRecordCount = subscriptionPlans.totalRecords;
      this.tablePageSize = 25;
      this.tablePageIndex = 1;
      this.loading = false;
      this.subscriptionPlanSearchForm.reset({});
      this.selectedAction = '';
      this.isActionLoading = false;
    });
  }

  onAdminUserInsertClick(event) {
    this.selectedAction = 'insert';
    this.pageScrollService.scroll({
      document: this.document,
      scrollTarget: '.table-data',
    });
  }

  fetchClientUsers(params) {
    return this.adminService.fetchUsers(params).pipe(
      take(1),
      map((response) => {
        const clientUserTableData: ClientUserTableData = {
          data: response.results.map((item) => {
            const clientUserTableItem: ClientUserTableDataItem = {
              id: item.id,
              firstName: item.first_name,
              lastName: item.last_name,
              email: item.email,
              address: item.profile
                ? item.profile.address
                  ? item.profile.address.displayText
                  : ''
                : '',
              subscriptionPlan: item.subscription_plan
                ? item.subscription_plan.plan
                  ? item.subscription_plan.plan.name
                  : ''
                : '',
              hasPaid: item.has_paid,
              paymentExpired: item.payment_expired,
            };
            return clientUserTableItem;
          }),
          totalPages: response.total_pages,
          totalRecords: response.total_records,
        };
        return clientUserTableData;
      })
    );
  }

  onClientUserUpdateClick(event) {
    this.isActionLoading = true;
    this.selectedAction = 'update';
    this.pageScrollService.scroll({
      document: this.document,
      scrollTarget: '.table-data',
    });
    this.adminService
      .fetchUser(this.selectedTableItemId)
      .subscribe((response) => {
        this.selectedTableItemData = response;
        const formValue = {
          firstName: response.first_name,
          lastName: response.last_name,
          email: response.email,
          phoneNumber: response.profile ? response.profile.phone_number : '',
          streetNumber: response.profile ? response.profile.street_number : '',
          city: response.profile ? response.profile.city : '',
          state: response.profile ? response.profile.state : '',
          zipCode: response.profile ? response.profile.zip_code : '',
        };
        this.clientUserUpdateForm.setValue(formValue);
        this.isActionLoading = false;
      });
  }

  onClientUserSearchClick(event) {
    this.selectedAction = 'search';
    this.pageScrollService.scroll({
      document: this.document,
      scrollTarget: '.table-data',
    });
  }

  onAdminUserInsertSubmitForm(event) {
    for (const i in this.adminUserInsertForm.controls) {
      this.adminUserInsertForm.controls[i].markAsDirty();
      this.adminUserInsertForm.controls[i].updateValueAndValidity();
    }
    this.isActionLoading = true;

    const {
      firstName,
      lastName,
      email,
      phoneNumber,
      streetNumber,
      city,
      state,
      zipCode,
      password,
    } = this.adminUserInsertForm.value;

    const params = {
      email,
      first_name: firstName,
      last_name: lastName,
      is_admin: true,
      profile: {
        phone_number: phoneNumber,
        address: null,
        street_number: streetNumber,
        city,
        state,
        zip_code: zipCode,
        is_preprocessed: false,
      },
      password,
    };

    this.adminService
      .insertUser(params)
      .pipe(
        take(1),
        catchError((error) => {
          this.notification.create('error', 'Error', 'Something went wrong.');
          return of(error);
        })
      )
      .subscribe((response) => {
        this.isActionLoading = false;
        this.notification.create(
          'success',
          'Success',
          'User added successfully!.',
          { nzPlacement: 'bottomRight' }
        );
        this.adminUserInsertForm.reset({});
        this.loading = true;
        this.selectedAction = '';
        this.adminUsers$ = this.fetchAdminUsers({ page: 1 });
        this.adminUsers$.subscribe((adminUsers) => {
          this.adminUsers = adminUsers;
          this.tableRecordCount = adminUsers.totalRecords;
          this.loading = false;
        });
      });
  }

  onAdminUserInsertCancelForm(event) {
    this.adminUserInsertForm.reset({});
    this.selectedAction = '';
  }

  onClientUserUpdateSubmitForm(event) {
    for (const i in this.clientUserUpdateForm.controls) {
      this.clientUserUpdateForm.controls[i].markAsDirty();
      this.clientUserUpdateForm.controls[i].updateValueAndValidity();
    }

    this.isActionLoading = true;

    const userId = this.selectedTableItemId;
    const userData = this.selectedTableItemData;

    const address = userData.profile
      ? userData.profile.address
        ? userData.profile.address
        : null
      : null;

    const isPreprocessed = userData.profile
      ? userData.profile.is_preprocessed
        ? userData.profile.is_preprocessed
        : false
      : false;

    const {
      firstName,
      lastName,
      email,
      phoneNumber,
      streetNumber,
      city,
      state,
      zipCode,
    } = this.clientUserUpdateForm.value;

    const params = {
      email,
      first_name: firstName,
      last_name: lastName,
      profile: {
        phone_number: phoneNumber,
        address,
        street_number: streetNumber,
        city,
        state,
        zip_code: zipCode,
        is_preprocessed: isPreprocessed,
      },
    };

    this.adminService
      .updateUser(userId, params)
      .pipe(
        take(1),
        catchError((error) => {
          this.notification.create('error', 'Error', 'Something went wrong.');
          return of(error);
        })
      )
      .subscribe((response) => {
        this.isActionLoading = false;
        this.notification.create(
          'success',
          'Success',
          'Data updated successfully!.',
          { nzPlacement: 'bottomRight' }
        );
        this.clientUserUpdateForm.reset({});
        this.loading = true;
        this.selectedAction = '';
        this.clientUsers$ = this.fetchClientUsers({
          page: this.tablePageIndex,
        });
        this.clientUsers$.subscribe((clientUsers) => {
          this.clientUsers = clientUsers;
          this.loading = false;
        });
      });
  }

  onClientUserSearchSubmitForm(event) {
    for (const i in this.clientUserSearchForm.controls) {
      this.clientUserSearchForm.controls[i].markAsDirty();
      this.clientUserSearchForm.controls[i].updateValueAndValidity();
    }

    this.isActionLoading = true;

    const { firstName, lastName, email } = this.clientUserSearchForm.value;

    const params = {
      email,
      first_name: firstName,
      last_name: lastName,
    };

    this.clientUsers$ = this.fetchClientUsers(params);
    this.clientUsers$.subscribe((clientUsers) => {
      this.clientUsers = clientUsers;
      this.tableRecordCount = clientUsers.totalRecords;
      this.tablePageSize = 25;
      this.tablePageIndex = 1;
      this.loading = false;
      this.clientUserSearchForm.reset({});
      this.selectedAction = '';
      this.isActionLoading = false;
    });
  }

  onClientUserSearchCancelForm(event) {
    this.clientUserSearchForm.reset({});
    this.selectedAction = '';
  }

  onClientUserUpdateCancelForm(event) {
    this.clientUserUpdateForm.reset({});
    this.selectedAction = '';
    this.selectedTableItemData = null;
  }

  onUserDataDeleteConfirm() {
    this.loading = true;

    const userId = this.selectedTableItemId;
    this.adminService
      .deleteUser(userId)
      .pipe(
        take(1),
        catchError((error) => {
          this.notification.create('error', 'Error', 'Something went wrong.');
          return of(error);
        })
      )
      .subscribe((response) => {
        this.loading = false;
        this.notification.create(
          'success',
          'Success',
          'User deleted successfully!.',
          { nzPlacement: 'bottomRight' }
        );
        this.clientUsers$ = this.fetchClientUsers({
          page: this.tablePageIndex,
        });
        this.clientUsers$.subscribe((clientUsers) => {
          this.clientUsers = clientUsers;
          this.loading = false;
        });
      });
  }
}
