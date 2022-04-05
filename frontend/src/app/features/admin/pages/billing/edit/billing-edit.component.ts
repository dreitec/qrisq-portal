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
  states = states;
  validateForm!: FormGroup;
  @Input() item?: AdminBillingItem;

  constructor(private modal: NzModalRef, private fb: FormBuilder) {}

  ngOnInit(): void {
    this.validateForm = this.fb.group({
      id: this.item?.id,
      type: [this.item?.type, [Validators.required]],
      city: this.item?.city,
      country: this.item?.country,
      state: [this.item?.state, [Validators.required]],
      startDate: this.item?.startDate || new Date(),
      endDate: this.item?.endDate,
      discount: [this.item?.discount, [Validators.min(0), Validators.max(100)]],
    });
  }

  disabledStartDate = (current: Date): boolean =>
    differenceInCalendarDays(current, new Date()) < 0;

  disabledEndDate = (current: Date): boolean =>
    differenceInCalendarDays(current, new Date()) < 0;

  closeModal(): void {
    this.modal.destroy();
  }

  submitForm(): void {
    this.modal.destroy({ data: this.validateForm.value });
  }
}
