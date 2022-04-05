import {
  Component,
  EventEmitter,
  HostListener,
  Input,
  OnInit,
  Output,
} from '@angular/core';

@Component({
  selector: 'qr-admin-layout',
  templateUrl: './layout.component.html',
  styleUrls: ['./layout.component.scss'],
})
export class QrAdminLayoutComponent {
  public isMenuCollapsed = true;
  @Output() logout = new EventEmitter<Event>();

  constructor() {}

  ngOnInit(): void {}

  onLogout($event) {
    this.logout.emit($event);
  }
}
