// angular
import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';

// modules
import { QrCoreModule } from '@app/core/core.module';
import { QrDesignModule } from '@app/design/design.module';
import { QrSharedModule } from '@app/shared/shared.module';
import { QrAdminService } from './services/admin.service';

// ngx-page-scroll-core
import { NgxPageScrollCoreModule } from 'ngx-page-scroll-core';

import { QrAdminRoutingModule } from './admin-routing.module';

// pages
import { QrAdminLayoutComponent } from '@app/features/admin/pages/layout/layout.component';
import { QrAdminDashboardComponent } from './pages/dashboard/dashboard.component';
import { QrAdminAdministratorsComponent } from './pages/administrators/administrators.component';
import { QrAdminUsersComponent } from './pages/users/users.component';
import { QrAdminBillingComponent } from './pages/billing/billing.component';
import { QrAdminSettingsComponent } from './pages/settings/settings.component';
import { QrAdminPanelPageComponent } from './pages/admin-panel/admin-panel.component';

// components
import { QrAdminPanelClientUserSearchComponent } from './components/qr-admin-panel-client-user-search/qr-admin-panel-client-user-search.component';
import { QrAdminPanelSubscriptionPlanSearchComponent } from './components/qr-admin-panel-subscription-plan-search/qr-admin-panel-subscription-plan-search.component';
import { QrAdminPanelSubscriptionPlanUpdateComponent } from './components/qr-admin-panel-subscription-plan-update/qr-admin-panel-subscription-plan-update.component';
import { QrAdminPanelSubscriptionPlanInsertComponent } from './components/qr-admin-panel-subscription-plan-insert/qr-admin-panel-subscription-plan-insert.component';

@NgModule({
  declarations: [
    QrAdminPanelPageComponent,
    QrAdminLayoutComponent,
    QrAdminDashboardComponent,
    QrAdminAdministratorsComponent,
    QrAdminUsersComponent,
    QrAdminBillingComponent,
    QrAdminSettingsComponent,
    QrAdminPanelClientUserSearchComponent,
    QrAdminPanelSubscriptionPlanSearchComponent,
    QrAdminPanelSubscriptionPlanUpdateComponent,
    QrAdminPanelSubscriptionPlanInsertComponent,
  ],
  imports: [
    CommonModule,
    FormsModule,
    ReactiveFormsModule,

    QrCoreModule,
    QrDesignModule,
    QrSharedModule,

    NgxPageScrollCoreModule,

    QrAdminRoutingModule,
  ],
  exports: [
    QrAdminPanelPageComponent,
    QrAdminDashboardComponent,
    QrAdminAdministratorsComponent,
    QrAdminUsersComponent,
    QrAdminBillingComponent,
    QrAdminSettingsComponent,
    QrAdminLayoutComponent,
  ],
  providers: [QrAdminService],
})
export class QrAdminModule {}
