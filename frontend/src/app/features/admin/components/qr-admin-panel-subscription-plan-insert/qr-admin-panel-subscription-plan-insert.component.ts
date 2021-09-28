import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core';
import { FormGroup } from '@angular/forms';

@Component({
  selector: 'qr-admin-panel-subscription-plan-insert',
  templateUrl: './qr-admin-panel-subscription-plan-insert.component.html',
  styleUrls: ['./qr-admin-panel-subscription-plan-insert.component.scss'],
})
export class QrAdminPanelSubscriptionPlanInsertComponent implements OnInit {
  @Input() formGroup: FormGroup;
  @Output() insertSubscriptionPlanSubmit = new EventEmitter();
  @Output() insertSubscriptionPlanCancel = new EventEmitter();

  constructor() {}

  ngOnInit() {}

  onSubmit(event) {
    this.insertSubscriptionPlanSubmit.emit();
  }

  onCancel(event) {
    this.insertSubscriptionPlanCancel.emit();
  }
}
