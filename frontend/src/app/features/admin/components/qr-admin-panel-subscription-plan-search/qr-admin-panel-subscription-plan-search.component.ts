import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core';
import { FormGroup } from '@angular/forms';

@Component({
  selector: 'qr-admin-panel-subscription-plan-search',
  templateUrl: './qr-admin-panel-subscription-plan-search.component.html',
  styleUrls: ['./qr-admin-panel-subscription-plan-search.component.scss'],
})
export class QrAdminPanelSubscriptionPlanSearchComponent implements OnInit {
  @Input() formGroup: FormGroup;
  @Output() subscriptionPlanSearchSubmit = new EventEmitter();
  @Output() subscriptionPlanSearchCancel = new EventEmitter();

  constructor() {}

  ngOnInit() {}

  onSubmit(event) {
    this.subscriptionPlanSearchSubmit.emit();
  }

  onCancel(event) {
    this.subscriptionPlanSearchCancel.emit();
  }
}
