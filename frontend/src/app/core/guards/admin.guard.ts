// angular
import { Injectable } from '@angular/core';
import {
  ActivatedRouteSnapshot,
  CanActivate,
  Router,
  RouterStateSnapshot,
} from '@angular/router';

// store, ngrx, rxjs
import { Store } from '@ngrx/store';
import { map, take } from 'rxjs/operators';

// state
import { SignedUserState } from '@app/features/identity/store/identity.models';
import { selectSignedUser } from '@app/features/identity/store/identity.selectors';

@Injectable()
export class QrAdminGuard implements CanActivate {
  constructor(private store: Store, private router: Router) {}

  canActivate(route: ActivatedRouteSnapshot, state: RouterStateSnapshot) {
    return this.store.select(selectSignedUser).pipe(
      take(1),
      map((user: SignedUserState) => {
        if (!user) {
          this.router.navigate(['/identity/login']);
        }
        return true;
      })
    );
  }
}
