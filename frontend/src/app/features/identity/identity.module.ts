// angular
import { BrowserModule } from '@angular/platform-browser';
import { CommonModule } from '@angular/common';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { HttpClientModule } from '@angular/common/http';
import { NgModule } from '@angular/core';

// routing
import { RouterModule } from '@angular/router';

// agm
import { AgmCoreModule } from '@agm/core';
import { GooglePlaceModule } from 'ngx-google-places-autocomplete';
import { NgxPayPalModule } from 'ngx-paypal';
import { CreditCardDirectivesModule } from 'angular-cc-library';

// core, design & shared
import { QrCoreModule } from '@core/core.module';
import { QrDesignModule } from '@app/design/design.module';
import { QrSharedModule } from '@shared/shared.module';

// component store
import { QrCheckServiceAreaComponentStore } from './pages/check-service-area/check-service-area.component-store';

// pages
import { QrAccountCreatedPageComponent } from './pages/account-created/account-created.component';
import { QrCheckServiceAreaPageComponent } from './pages/check-service-area/check-service-area.component';
import { QrGeolocationPageComponent } from './pages/geolocation/geolocation.component';
import { QrLoginPageComponent } from './pages/login-page/login-page.component';
import { QrPaymentPageComponent } from './pages/payment/payment.component';
import { QrPaymentSuccessfulPageComponent } from './pages/payment-successful/payment-successful.component';
import { QrRegisterPageComponent } from './pages/register/register-page.component';
import { QrServiceAreaAvailablePageComponent } from './pages/service-area-available/service-area-available.component';
import { QrServiceAreaUnavailablePageComponent } from './pages/service-area-unavailable/service-area-unavailable.component';

// services
import { QrGeocodingService } from './services/geocode.service';
import { QrIdentityService } from './services/identity.service';
import { QrPaymentService } from './services/payment.service';

// components
import { QrGeolocationAddressComponent } from './components/geolocation-address/geolocation-address.component';
import { QrPaymentFormCardComponent } from './components/payment-form-credit-card/payment-form-credit-card.component';
import { QrPaymentFormPaypalComponent } from './components/payment-form-paypal/payment-form-paypal.component';
import { QrGeolocationService } from './services/geolocation.service';
import { QrContactInformationPageComponent } from './pages/contact-information/contact-information.component';
import { QrForgotPasswordPageComponent } from './pages/forgot-password/forgot-password.component';
import { QrResetPasswordPageComponent } from './pages/reset-password/reset-password.component';
import { QrCancelSubscriptionPageComponent } from './pages/cancel-subscription/cancel-subscription.component';

@NgModule({
  declarations: [
    // pages
    QrAccountCreatedPageComponent,
    QrCheckServiceAreaPageComponent,
    QrGeolocationPageComponent,
    QrLoginPageComponent,
    QrPaymentPageComponent,
    QrRegisterPageComponent,
    QrServiceAreaAvailablePageComponent,
    QrServiceAreaUnavailablePageComponent,
    QrContactInformationPageComponent,
    QrResetPasswordPageComponent,
    QrCancelSubscriptionPageComponent,

    // components
    QrGeolocationAddressComponent,
    QrPaymentFormCardComponent,
    QrPaymentFormPaypalComponent,
    QrPaymentSuccessfulPageComponent,
    QrForgotPasswordPageComponent,
  ],
  imports: [
    // angular
    CommonModule,
    HttpClientModule,
    FormsModule,
    ReactiveFormsModule,

    // routing
    RouterModule,

    // modules
    QrCoreModule,
    QrDesignModule,
    QrSharedModule,

    // agm
    AgmCoreModule.forRoot({
      apiKey: 'AIzaSyCWrBf7hkK6LQdlv7ul98DzcyoFdF1OzLM',
    }),

    // google maps
    GooglePlaceModule,

    // paypal
    NgxPayPalModule,

    // angular-cc-library
    CreditCardDirectivesModule,
  ],
  providers: [
    QrIdentityService,
    QrGeocodingService,
    QrPaymentService,
    QrGeolocationService,
    QrCheckServiceAreaComponentStore,
  ],
  exports: [
    QrAccountCreatedPageComponent,
    QrCheckServiceAreaPageComponent,
    QrGeolocationPageComponent,
    QrPaymentFormPaypalComponent,
    QrPaymentPageComponent,
    QrRegisterPageComponent,
    QrServiceAreaAvailablePageComponent,
    QrServiceAreaAvailablePageComponent,
    QrServiceAreaUnavailablePageComponent,
    QrContactInformationPageComponent,
    QrForgotPasswordPageComponent,
    QrResetPasswordPageComponent,
    QrCancelSubscriptionPageComponent,
  ],
})
export class QrIdentityModule {}
