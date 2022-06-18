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
import { selectSignedUser } from '@app/features/identity/store/identity.selectors';

@Injectable()
export class QrPaymentGuard implements CanActivate {
  constructor(private store: Store, private router: Router) {}

  canActivate(route: ActivatedRouteSnapshot, state: RouterStateSnapshot) {
    return this.store.select(selectSignedUser).pipe(
      map((signedUser) => {
        if (!signedUser) {
          return this.router.parseUrl('identity/login');
        }

        if (!signedUser.user.isAdmin && !signedUser.user.hasPaid) {
          return this.router.parseUrl('identity/sign-up/payment');
        }
        return true;
      })
    );
  }
}
