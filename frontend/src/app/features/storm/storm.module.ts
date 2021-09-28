// angular
import { AgmCoreModule, GoogleMapsAPIWrapper } from '@agm/core';
import { CommonModule } from '@angular/common';
import { NgModule } from '@angular/core';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { RouterModule } from '@angular/router';

import { QrStormService } from './services/storm.service';

import { QrStormPageComponent } from './pages/storm/storm-page.component';
import { QrStormMapComponent } from './components/qr-storm-map/qr-storm-map.component';
import { QrStormDataComponent } from './components/qr-storm-data/qr-storm-data.component';
import { QrCoreModule } from '@app/core/core.module';
import { QrDesignModule } from '@app/design/design.module';
import { QrSharedModule } from '@app/shared/shared.module';
import { QrStormFreePageComponent } from './pages/storm-free/storm-free.component';
import { QrStormMapIconComponent } from './components/qr-storm-map-icon/qr-storm-map-icon.component';
import { QrStormMapNoDataComponent } from './components/qr-storm-map-no-data/qr-storm-map-no-data.component';

// pages
// components
// google maps
// core, design & shared
@NgModule({
  declarations: [
    QrStormPageComponent,
    QrStormFreePageComponent,
    QrStormMapComponent,
    QrStormDataComponent,
    QrStormMapIconComponent,
    QrStormMapNoDataComponent,
  ],

  imports: [
    CommonModule,
    FormsModule,
    ReactiveFormsModule,
    RouterModule,

    QrCoreModule,
    QrDesignModule,
    QrSharedModule,

    AgmCoreModule.forRoot({
      apiKey: 'AIzaSyCWrBf7hkK6LQdlv7ul98DzcyoFdF1OzLM',
    }),
  ],
  providers: [QrStormService, GoogleMapsAPIWrapper],
  exports: [QrStormPageComponent, QrStormFreePageComponent],
})
export class QrStormModule {}
