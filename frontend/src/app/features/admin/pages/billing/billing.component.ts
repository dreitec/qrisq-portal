import { Component, OnInit } from '@angular/core';
import { NzModalService } from 'ng-zorro-antd/modal';
import moment from 'moment';
import { of } from 'rxjs';
import { states } from '../../store/states';
import { QrAdminService } from '../../services/admin.service';
import { AdminBillingItem } from '../../models/AdminUser.models';
import { QrAdminBillingEditComponent } from './edit/billing-edit.component';
import { catchError, map, take } from 'rxjs/operators';
import { NzNotificationService } from 'ng-zorro-antd/notification';
import { getBillingStatus, TimeUtils } from '@app/features/storm/common/utils';

@Component({
  selector: 'qr-admin-billing',
  templateUrl: './billing.component.html',
  styleUrls: ['./billing.component.scss'],
})
export class QrAdminBillingComponent implements OnInit {
  states = states;
  data: AdminBillingItem[] = [];
  items: AdminBillingItem[] = [];
  filterType = '';
  filterCity = '';
  filterCounty = '';
  filterState = '';
  filterStatus = null;

  constructor(
    private adminService: QrAdminService,
    private modal: NzModalService,
    private notification: NzNotificationService
  ) {}

  ngOnInit(): void {
    this.adminService
      .fetchBilling()
      .pipe(
        take(1),
        map((response) => response)
      )
      .subscribe((data) => {
        this.data = data.results.map(item => ({
          ...item,
          status: getBillingStatus(item.start_date, item.end_date),
        }));
        this.filterData();
      });
  }

  filterData() {
    this.items = this.data.filter((item) => {
      if (this.filterType) {
        if (item.type !== this.filterType) { return false; }
      }
      const city = this.filterCity.trim();
      if (city) {
        if (item.type === 'C' && !item.city.includes(city)) { return false; }
      }
      if (this.filterState) {
        if (item.type === 'S' && item.state !== this.filterState) { return false; }
      }
      const county = this.filterCounty.trim();
      if (county) {
        if (item.type === 'P' && !item.county.includes(county)) { return false; }
      }
      if (this.filterStatus) {
        if (item.status !== this.filterStatus) { return false; }
      }
      return true;
    });
  }

  clearFilters(): void {
    this.filterType = '';
    this.filterCity = '';
    this.filterCounty = '';
    this.filterState = '';
    this.filterStatus = '';
    this.filterData();
  }

  getType(item) {
    return {
      C: 'City',
      S: 'State',
      P: 'County',
    }[item.type];
  }

  getStatus(item) {
    return {
      [0]: 'Pending',
      [1]: 'Active',
      [-1]: 'Expired',
    }[item.status];
  }

  dateToString(date) {
    return date ? moment(date).format('MM/DD/yy') : '';
  }

  discountToString(discount) {
    return discount ? `${discount}%` : '';
  }

  showEdit(item?: AdminBillingItem): void {
    const modal = this.modal.create({
      nzMaskClosable: false,
      nzClosable: false,
      nzFooter: null,
      nzWidth: 680,
      nzContent: QrAdminBillingEditComponent,
      nzComponentParams: {
        item,
      },
    });

    modal.afterClose.subscribe((result) => {
      if (!result) { return; }

      const startDate = TimeUtils.toDefaultDate(result.data.start_date);
      const endDate = result.data.end_date ? TimeUtils.toDefaultDate(result.data.end_date) : '';

      const formData: FormData = new FormData();
      if (result.data.id) {
        formData.append('id', result.data.id);
      }
      formData.append('type', result.data.type);
      formData.append('city', result.data.city || '');
      formData.append('county', result.data.county || '');
      formData.append('state', result.data.state || '');
      formData.append('start_date', startDate);
      formData.append('end_date', endDate);
      formData.append('status', getBillingStatus(startDate, endDate).toString());
      formData.append('discount', result.data.discount || 100);
      formData.append('users', result.data.users || 0);
      if (result.data.file) {
        const fileNames = result.data.file.name.split('.');
        const newFileName = `${fileNames.slice(0, fileNames.length - 1)}_${new Date().getTime()}.${fileNames[fileNames.length - 1]}`;
        formData.append('file', result.data.file, newFileName);
      }

      if (result.data.id) {
        this.adminService
          .updateBilling(result.data.id, formData)
          .pipe(
            take(1),
            catchError((error) => {
              this.notification.create(
                'error',
                'Error',
                'Something went wrong.'
              );
              return of(error);
            })
          )
          .subscribe((response) => {
            this.notification.create(
              'success',
              'Success',
              'Billing updated successfully!.',
              { nzPlacement: 'bottomRight' }
            );
            this.data = this.data.map((item) =>
              item.id === result.data.id ? {
                ...response,
                status: getBillingStatus(response.start_date, response.end_date),
              } : item
            );
            this.filterData();
          });
      } else {
        this.adminService
          .addBilling(formData)
          .pipe(
            take(1),
            catchError((error) => {
              this.notification.create(
                'error',
                'Error',
                'Something went wrong.'
              );
              return of(error);
            })
          )
          .subscribe((response) => {
            this.notification.create(
              'success',
              'Success',
              'Billing added successfully!.',
              { nzPlacement: 'bottomRight' }
            );
            this.data = [
              {
                ...response,
                status: getBillingStatus(response.start_date, response.end_date),
              },
              ...this.data,
            ];
            this.filterData();
          });
      }
    });
  }

  showDeleteConfirm(item: AdminBillingItem): void {
    this.modal.confirm({
      nzTitle: `Are you sure delete this contract?`,
      nzContent: `Id: ${item.id}`,
      nzOkText: 'Delete',
      nzOkType: 'primary',
      nzOkDanger: true,
      nzOnOk: () => {
        this.adminService
          .deleteBilling(item.id)
          .pipe(
            take(1),
            catchError((error) => {
              this.notification.create(
                'error',
                'Error',
                'Something went wrong.'
              );
              return of(error);
            })
          )
          .subscribe(() => {
            this.notification.create(
              'success',
              'Success',
              'Billing deleted successfully!.',
              { nzPlacement: 'bottomRight' }
            );
            this.data = this.data.filter(({ id }) => id !== item.id);
            this.filterData();
          });
      },
    });
  }
}
