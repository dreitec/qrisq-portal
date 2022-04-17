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
  filterCountry = '';
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
        this.data = data.results;
        this.filterData();
      });
  }

  filterData() {
    this.items = this.data.filter((item) => {
      if (this.filterType) {
        if (item.type !== this.filterType) return false;
      }
      const _city = this.filterCity.trim();
      if (_city) {
        if (item.type === 'C' && !item.name.includes(_city)) return false;
      }
      if (this.filterState) {
        if (item.type === 'S' && item.name !== this.filterState) return false;
      }
      const _country = this.filterCountry.trim();
      if (_country) {
        if (item.type === 'P' && !item.name.includes(_country)) return false;
      }
      if (this.filterStatus) {
        if (item.status !== this.filterStatus) return false;
      }
      return true;
    });
  }

  clearFilters(): void {
    this.filterType = '';
    this.filterCity = '';
    this.filterCountry = '';
    this.filterState = '';
    this.filterStatus = '';
    this.filterData();
  }

  getType(item) {
    return {
      C: 'City',
      S: 'State',
      P: 'Country',
    }[item.type];
  }

  getState(item) {
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
      if (!result) return;

      const newItem: AdminBillingItem = {
        ...result.data,
        name: result.data.city || result.data.country || result.data.state,
        status: result.data.status || 0,
        discount: result.data.discount || 0,
        users: 0,
      };

      if (newItem.id) {
        this.adminService
          .updateBilling(newItem.id, newItem)
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
              item.id === newItem.id ? response : item
            );
            this.filterData();
          });
      } else {
        this.adminService
          .addBilling({
            ...newItem,
            status: newItem.status || 0,
            discount: newItem.discount || 0,
          })
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
            this.data = [response, ...this.data];
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
