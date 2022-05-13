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
  fileToUpload: File | null = null;
  @Input() item?: AdminBillingItem;

  constructor(private modal: NzModalRef, private fb: FormBuilder) {}

  ngOnInit(): void {
    const type = this.item?.type;
    const city = this.item?.city;
    const county = this.item?.county;
    const state = this.item?.state;
    console.log('type = ', type);
    this.form = this.fb.group({
      id: this.item?.id,
      type: [type || '', [Validators.required]],
      city: {
        value: type === 'C' ? city : '',
        disabled: type !== 'C',
      },
      county: {
        value: type === 'P' ? county : '',
        disabled: type !== 'P',
      },
      state: {
        value: type === 'S' ? state : '',
        disabled: type !== 'S',
      },
      startDate: this.item?.startDate || new Date(),
      endDate: this.item?.endDate,
      discount: {
        value: this.item?.discount || 100,
        disabled: true,
      },
    });
  }

  changeType(type) {
    this.form.controls.city.disable();
    this.form.controls.city.setValue('');
    this.form.controls.county.disable();
    this.form.controls.county.setValue('');
    this.form.controls.state.disable();
    this.form.controls.state.setValue('');
    if (type === 'C') {
      this.form.controls.city.enable();
      this.form.controls.state.enable();
    }
    if (type === 'P') {
      this.form.controls.county.enable();
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

  handleFileInput(event: any): void {
    if (event.target.files) {
      this.fileToUpload = event.target.files.item(0);
    }
  }
  
  submitForm(): void {
    console.log('this.fileToUpload: ', this.fileToUpload);
    this.modal.destroy({ data: { ...this.form.value, file: this.fileToUpload } });
  }
}
