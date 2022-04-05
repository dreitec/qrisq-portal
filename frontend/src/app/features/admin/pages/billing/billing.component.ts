import { Component, OnInit } from '@angular/core';
import { NzModalService } from 'ng-zorro-antd/modal';
import moment from 'moment';
import { AdminBillingItem } from '../../models/AdminUser.models';
import { QrAdminBillingEditComponent } from './edit/billing-edit.component';
import { states } from '../../store/states';

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
  filterStatus = '';

  constructor(private modal: NzModalService) {}

  ngOnInit(): void {}

  filterData() {
    this.items = this.data.filter((item) => {
      if (this.filterType) {
        if (item.type !== this.filterType) return false;
      }
      const _city = this.filterCity.trim();
      if (_city) {
        if (!item.city.includes(_city)) return false;
      }
      const _country = this.filterCountry.trim();
      if (_country) {
        if (!item.country.includes(_country)) return false;
      }
      if (this.filterState) {
        if (item.state !== this.filterState) return false;
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
      nzWidth: 600,
      nzContent: QrAdminBillingEditComponent,
      nzComponentParams: {
        item,
      },
    });

    modal.afterClose.subscribe((result) => {
      if (!result) return;

      const newItem: AdminBillingItem = {
        ...result.data,
        status: '',
        users: 0,
      };

      if (newItem.id) {
        this.data = this.data.map((item) =>
          item.id === newItem.id ? newItem : item
        );
      } else {
        newItem.id = `${this.data.length + 1}`;
        this.data = [newItem, ...this.data];
      }
      this.filterData();
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
        this.data = this.data.filter(({ id }) => id !== item.id);
        this.filterData();
      },
    });
  }
}
