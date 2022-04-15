import {
  Component,
  EventEmitter,
  HostListener,
  Input,
  OnInit,
  Output,
} from '@angular/core';
import { Store } from '@ngrx/store';
import { actionSignOut } from '@app/features/identity/store/identity.actions';
import { CredentialsState } from '@app/features/identity/store/identity.models';
import { selectCredentials } from '@app/features/identity/store/identity.selectors';

@Component({
  selector: 'qr-admin-layout',
  templateUrl: './layout.component.html',
  styleUrls: ['./layout.component.scss'],
})
export class QrAdminLayoutComponent {
  public isMenuCollapsed = true;
  credentials: CredentialsState;
  @Output() logout = new EventEmitter<Event>();

  constructor(
    private store: Store,
  ) {}

  ngOnInit(): void {
    this.store
    .select(selectCredentials)
    .subscribe((credentials: CredentialsState) => {
      if (credentials) {
        this.credentials = credentials;
      }
    });
  }

  onLogout($event) {
    const refreshToken = this.credentials.refreshToken;
    this.store.dispatch(actionSignOut({ refreshToken }));
  }
}
