// angular
import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

// components
import { AppComponent } from './app.component';

// pages
import { QrMainLayoutComponent } from './pages/main/main.component';
import { QrAccountCreatedPageComponent } from './features/identity/pages/account-created/account-created.component';
import { QrCheckServiceAreaPageComponent } from './features/identity/pages/check-service-area/check-service-area.component';
import { QrFaqPageComponent } from './pages/storm-data/faq-page/faq-page.component';
import { QrForecastPageComponent } from './pages/storm-data/forecast-page/forecast-page.component';
import { QrGeolocationPageComponent } from './features/identity/pages/geolocation/geolocation.component';
import { QrGovernmentPageComponent } from './pages/services/government-page/government.component';
import { QrHindcastPageComponent } from './pages/storm-data/hindcast-page/hindcast-page.component';
import { QrHistoricalPageComponent } from './pages/storm-data/historical-page/historical-page.component';
import { QrHomeownersPageComponent } from './pages/services/homeowners-page/homeowners-page.component';
import { QrHomePageComponent } from './pages/home/home-page.component';
import { QrInsurancePageComponent } from './pages/services/insurance-page/insurance-page.component';
import { QrLoginPageComponent } from './features/identity/pages/login-page/login-page.component';
import { QrPaymentPageComponent } from './features/identity/pages/payment/payment.component';
import { QrRegisterPageComponent } from './features/identity/pages/register/register-page.component';
import { QrServiceAreaAvailablePageComponent } from './features/identity/pages/service-area-available/service-area-available.component';
import { QrStormPageComponent } from './features/storm/pages/storm/storm-page.component';
import { QrStormFreePageComponent } from './features/storm/pages/storm-free/storm-free.component';
import { QrServiceAreaUnavailablePageComponent } from './features/identity/pages/service-area-unavailable/service-area-unavailable.component';
import { QrContactUsPageComponent } from './features/contact-us/pages/contact-us/contact-us.component';
import { QrContactInformationPageComponent } from './features/identity/pages/contact-information/contact-information.component';
import { QrForgotPasswordPageComponent } from './features/identity/pages/forgot-password/forgot-password.component';
import { QrResetPasswordPageComponent } from './features/identity/pages/reset-password/reset-password.component';
import { QrCancelSubscriptionPageComponent } from './features/identity/pages/cancel-subscription/cancel-subscription.component';
import { QrPaymentSuccessfulPageComponent } from './features/identity/pages/payment-successful/payment-successful.component';

// guard
import { QrAdminGuard } from './core/guards/admin.guard';
import { QrAuthGuard } from './core/guards/auth.guard';
import { QrNoAuthGuard } from './core/guards/no-auth.guard';
import { QrPaymentGuard } from './core/guards/payment.guards';
import { QrGeolocationGuard } from './core/guards/geolocation.guard';

const routes: Routes = [
  /* ---------------------------------- main --------------------------------- */

  {
    path: '',
    component: QrMainLayoutComponent,
    children: [
      /* ---------------------------------- home ---------------------------------- */

      { path: '', component: QrHomePageComponent },

      /* --------------------------------- sign-up -------------------------------- */

      {
        path: 'identity/reset-password?token="lasdasd"',
        redirectTo: 'identity/sign-up/check-service-area',
        pathMatch: 'full',
      },

      {
        path: 'identity/sign-up',
        redirectTo: 'identity/sign-up/check-service-area',
        pathMatch: 'full',
      },
      {
        path: 'identity/sign-up/check-service-area',
        component: QrCheckServiceAreaPageComponent,
      },
      {
        path: 'identity/sign-up/service-area-available',
        component: QrServiceAreaAvailablePageComponent,
      },
      {
        path: 'identity/sign-up/service-area-unavailable',
        component: QrServiceAreaUnavailablePageComponent,
      },
      {
        path: 'identity/sign-up/register',
        component: QrRegisterPageComponent,
      },
      {
        path: 'identity/sign-up/account-created',
        component: QrAccountCreatedPageComponent,
      },
      {
        path: 'identity/sign-up/payment',
        component: QrPaymentPageComponent,
      },
      {
        path: 'identity/sign-up/payment-successful',
        component: QrPaymentSuccessfulPageComponent,
      },
      {
        path: 'identity/sign-up/geolocation',
        component: QrGeolocationPageComponent,
      },

      /* ---------------------------------- login --------------------------------- */

      {
        path: 'identity/login',
        component: QrLoginPageComponent,
      },

      /* --------------------------- contact-information -------------------------- */

      {
        path: 'identity/contact-information',
        component: QrContactInformationPageComponent,
        canActivate: [QrAuthGuard],
      },

      /* ----------------------------- forgot-password ---------------------------- */

      {
        path: 'identity/forgot-password',
        component: QrForgotPasswordPageComponent,
      },

      /* ----------------------------- reset-password ----------------------------- */

      {
        path: 'identity/reset-password',
        component: QrResetPasswordPageComponent,
      },

      /* --------------------------- cancel-subscription -------------------------- */

      {
        path: 'identity/cancel-subscription',
        component: QrCancelSubscriptionPageComponent,
        canActivate: [QrAuthGuard],
      },

      /* -------------------------------- services -------------------------------- */

      {
        path: 'services/homeowners',
        component: QrHomeownersPageComponent,
      },
      {
        path: 'services/government',
        component: QrGovernmentPageComponent,
      },
      {
        path: 'services/insurance',
        component: QrInsurancePageComponent,
      },

      /* ---------------------------------- storm --------------------------------- */

      {
        path: 'storm',
        component: QrStormPageComponent,
        canActivate: [QrAuthGuard, QrPaymentGuard, QrGeolocationGuard],
      },

      {
        path: 'storm-free',
        component: QrStormFreePageComponent,
      },

      /* ------------------------------- storm-data ------------------------------- */

      {
        path: 'storm-data/forecast',
        component: QrForecastPageComponent,
      },
      {
        path: 'storm-data/hindcast',
        component: QrHindcastPageComponent,
      },

      /* ------------------------------- contact-us ------------------------------- */
      {
        path: 'contact-us',
        component: QrContactUsPageComponent,
      },
    ],
  },

  /* ---------------------------------- admin --------------------------------- */

  {
    path: 'admin',
    loadChildren: () =>
      import('./features/admin/admin.module').then(
        ({ QrAdminModule }) => QrAdminModule
      ),
    canActivate: [QrAdminGuard],
  },

  /* ------------------------------------ - ----------------------------------- */

  { path: '**', redirectTo: '' },
];

@NgModule({
  imports: [
    RouterModule.forRoot(routes, {
      scrollPositionRestoration: 'enabled',
    }),
  ],
  exports: [RouterModule],
})
export class AppRoutingModule {}
