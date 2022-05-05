import { Injectable } from '@angular/core';
import {
  HttpHandler,
  HttpInterceptor,
  HttpRequest,
  HttpResponse,
} from '@angular/common/http';
import { Store } from '@ngrx/store';
import { Router } from '@angular/router';
import { selectCredentials } from '@app/features/identity/store/identity.selectors';
import { catchError, map, switchMap, take, tap } from 'rxjs/operators';
import { throwError } from 'rxjs';
import { QrIdentityService } from '@app/features/identity/services/identity.service';
import {
  actionAccessTokenRefreshed,
  actionSignOut,
} from '@app/features/identity/store/identity.actions';
import { environment } from '@env';

@Injectable()
export class AuthInterceptor implements HttpInterceptor {
  protectedUrls = [
    '/process-transaction',
    '/pin-drag-address',
    '/pin-drag-attempt',
    '/request-address-change',
    '/storm-data',
    '/auth/account-profile',
    '/create-subscription',
    '/cancel-subscription',
    '/verify-subscription-payment',
    '/admins',
    '/users',
    '/clients',
    '/subscription-plans',
    '/subscription-plans-discount',
    '/billing',
    '/global-config',
  ];

  constructor(
    private store: Store,
    private router: Router,
    private identityService: QrIdentityService
  ) {}

  addTokenToHeader(request: HttpRequest<any>, token): HttpRequest<any> {
    return request.clone({
      withCredentials: true,
      setHeaders: { Authorization: `Bearer ${token}` },
    });
  }

  isProtected(requestUrl: string): boolean {
    return this.protectedUrls.some((url) => requestUrl.includes(url));
  }

  intercept(request: HttpRequest<any>, next: HttpHandler): any {
    if (request.url.includes('/storm-data/free')) {
      return next.handle(
        request.clone({ url: environment.API_URL + '/storm-data' })
      );
    }

    if (
      request.url.includes('/subscription-plans') &&
      request.method === 'GET'
    ) {
      return next.handle(request.clone({ url: request.url }));
    }

    if (
      request.url.includes('/subscription-plans-discount') &&
      request.method === 'POST'
    ) {
      return next.handle(request.clone({ url: request.url }));
    }

    if (this.isProtected(request.url)) {
      return this.store.select(selectCredentials).pipe(
        take(1),
        tap((credentials) => console.log(credentials)),
        switchMap((credentials) => {
          if (!credentials) {
            this.router.navigate(['/identity/login']);
            return throwError('Unauthorized');
          } else {
            return this.identityService
              .refreshCredentials(credentials.refreshToken)
              .pipe(
                take(1),
                catchError((error) => {
                  this.store.dispatch(
                    actionSignOut({
                      refreshToken: credentials.refreshToken,
                    })
                  );
                  this.router.navigate(['/identity/login']);
                  return throwError(error);
                }),
                switchMap((response: { access: string }) => {
                  this.store.dispatch(
                    actionAccessTokenRefreshed({
                      newAccessToken: response.access,
                    })
                  );
                  return next.handle(
                    this.addTokenToHeader(request, response.access)
                  );
                })
              );
          }
        })
      );
    } else {
      return next.handle(request);
    }
  }
}
