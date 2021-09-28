import { Component, Input, OnInit, Output, EventEmitter } from '@angular/core';
import { FormGroup } from '@angular/forms';

@Component({
  selector: 'qr-admin-panel-client-user-search',
  templateUrl: './qr-admin-panel-client-user-search.component.html',
  styleUrls: ['./qr-admin-panel-client-user-search.component.scss'],
})
export class QrAdminPanelClientUserSearchComponent implements OnInit {
  @Input() formGroup: FormGroup;
  @Output() searchClientUserSubmit = new EventEmitter();
  @Output() searchClientUserCancel = new EventEmitter();

  constructor() {}

  ngOnInit() {}

  onSubmit(event) {
    this.searchClientUserSubmit.emit();
  }

  onCancel(event) {
    this.searchClientUserCancel.emit();
  }
}
