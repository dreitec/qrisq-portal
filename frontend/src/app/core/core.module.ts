// angular
import { NgModule } from '@angular/core';
import { AuthInterceptor } from './interceptors/auth.interceptor';
import { QrAuthGuard } from './guards/auth.guard';
import { HTTP_INTERCEPTORS } from '@angular/common/http';
import { QrNoAuthGuard } from './guards/no-auth.guard';
import { QrPaymentGuard } from './guards/payment.guards';
import { QrAdminGuard } from './guards/admin.guard';
import { QrGeolocationGuard } from './guards/geolocation.guard';

@NgModule({
  declarations: [],
  imports: [],
  exports: [],
  providers: [
    QrAuthGuard,
    QrNoAuthGuard,
    QrPaymentGuard,
    {
      provide: HTTP_INTERCEPTORS,
      useClass: AuthInterceptor,
      multi: true,
    },
    QrAdminGuard,
    QrGeolocationGuard,
  ],
})
export class QrCoreModule {}
