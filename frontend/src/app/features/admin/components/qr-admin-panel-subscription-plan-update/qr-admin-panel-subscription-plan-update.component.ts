import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core';
import { FormGroup } from '@angular/forms';

@Component({
  selector: 'qr-admin-panel-subscription-plan-update',
  templateUrl: './qr-admin-panel-subscription-plan-update.component.html',
  styleUrls: ['./qr-admin-panel-subscription-plan-update.component.scss'],
})
export class QrAdminPanelSubscriptionPlanUpdateComponent implements OnInit {
  @Input() formGroup: FormGroup;
  @Output() updateSubmit = new EventEmitter();
  @Output() updateCancel = new EventEmitter();

  constructor() {}

  ngOnInit() {}

  onSubmit(event) {
    this.updateSubmit.emit();
  }

  onCancel(event) {
    this.updateCancel.emit();
  }
}
