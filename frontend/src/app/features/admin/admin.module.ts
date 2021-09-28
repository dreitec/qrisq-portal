// angular
import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { RouterModule } from '@angular/router';

// modules
import { QrCoreModule } from '@app/core/core.module';
import { QrDesignModule } from '@app/design/design.module';
import { QrSharedModule } from '@app/shared/shared.module';
import { QrAdminService } from './services/admin.service';

// ngx-page-scroll-core
import { NgxPageScrollCoreModule } from 'ngx-page-scroll-core';

// pages
import { QrAdminPanelPageComponent } from './pages/admin-panel/admin-panel.component';

// components
import { QrAdminPanelClientUserSearchComponent } from './components/qr-admin-panel-client-user-search/qr-admin-panel-client-user-search.component';
import { QrAdminPanelSubscriptionPlanSearchComponent } from './components/qr-admin-panel-subscription-plan-search/qr-admin-panel-subscription-plan-search.component';
import { QrAdminPanelSubscriptionPlanUpdateComponent } from './components/qr-admin-panel-subscription-plan-update/qr-admin-panel-subscription-plan-update.component';
import { QrAdminPanelSubscriptionPlanInsertComponent } from './components/qr-admin-panel-subscription-plan-insert/qr-admin-panel-subscription-plan-insert.component';

@NgModule({
  declarations: [
    QrAdminPanelPageComponent,
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
  ],
  exports: [QrAdminPanelPageComponent],
  providers: [QrAdminService],
})
export class QrAdminModule {}
