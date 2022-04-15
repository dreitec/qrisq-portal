import { Component, Input, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { AdminBillingItem } from '@app/features/admin/models/AdminUser.models';
import { NzModalRef } from 'ng-zorro-antd/modal';
import { differenceInCalendarDays } from 'date-fns';
import { states } from '../../../store/states';

@Component({
  selector: 'qr-admin-billing-edit',
  templateUrl: './billing-edit.component.html',
  styleUrls: ['./billing-edit.component.scss'],
})
export class QrAdminBillingEditComponent implements OnInit {
  type: string;
  states = states;
  form!: FormGroup;
  @Input() item?: AdminBillingItem;

  constructor(private modal: NzModalRef, private fb: FormBuilder) {}

  ngOnInit(): void {
    const type = this.item?.type;
    const name = this.item?.name;
    this.form = this.fb.group({
      id: this.item?.id,
      type: [type, [Validators.required]],
      city: {
        value: type === 'C' ? name : '',
        disabled: type !== 'C',
      },
      country: {
        value: type === 'P' ? name : '',
        disabled: type !== 'P',
      },
      state: {
        value: type === 'S' ? name : '',
        disabled: type !== 'S',
      },
      startDate: this.item?.startDate || new Date(),
      endDate: this.item?.endDate,
      discount: [this.item?.discount, [Validators.min(0), Validators.max(100)]],
    });
  }

  changeType(type) {
    this.form.controls.city.disable();
    this.form.controls.city.setValue('');
    this.form.controls.country.disable();
    this.form.controls.country.setValue('');
    this.form.controls.state.disable();
    this.form.controls.state.setValue('');
    if (type === 'C') {
      this.form.controls.city.enable();
    }
    if (type === 'P') {
      this.form.controls.country.enable();
    }
    if (type === 'S') {
      this.form.controls.state.enable();
    }
  }

  disabledStartDate(current: Date): boolean {
    return differenceInCalendarDays(current, new Date()) < 0;
  }

  disabledEndDate(current: Date): boolean {
    return differenceInCalendarDays(current, new Date()) < 0;
  }

  closeModal(): void {
    this.modal.destroy();
  }

  submitForm(): void {
    this.modal.destroy({ data: this.form.value });
  }
}
