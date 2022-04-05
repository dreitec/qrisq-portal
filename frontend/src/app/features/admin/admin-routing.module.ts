import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { QrAdminLayoutComponent } from './pages/layout/layout.component';
import { QrAdminDashboardComponent } from './pages/dashboard/dashboard.component';
import { QrAdminAdministratorsComponent } from './pages/administrators/administrators.component';
import { QrAdminUsersComponent } from './pages/users/users.component';
import { QrAdminBillingComponent } from './pages/billing/billing.component';
import { QrAdminSettingsComponent } from './pages/settings/settings.component';

const routes: Routes = [
  {
    path: '',
    component: QrAdminLayoutComponent,
    children: [
      {
        path: '',
        component: QrAdminDashboardComponent,
      },
      {
        path: 'administrators',
        component: QrAdminAdministratorsComponent,
      },
      {
        path: 'users',
        component: QrAdminUsersComponent,
      },
      {
        path: 'billing',
        component: QrAdminBillingComponent,
      },
      {
        path: 'settings',
        component: QrAdminSettingsComponent,
      },
      { path: '**', redirectTo: '' },
    ],
  },
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule],
})
export class QrAdminRoutingModule {}
