// angular
import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';

// design
import { QrDesignModule } from '@app/design/design.module';

// bootstrap
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';

// components
import { QrBannerComponent } from './components/banner/banner.component';
import { QrContentComponent } from './components/content/content.component';
import { QrHeaderComponent } from './components/header/header.component';
import { QrLayoutComponent } from './components/layout/layout.component';
import { QrFooterComponent } from './components/footer/footer.component';
import { QrTrackStormCardComponent } from './components/cards/track-storm/track-storm.component';
import { QrContactUsFormComponent } from './components/forms/contact-us/contact-us.component';
import { QrOurServicesCardComponent } from './components/cards/our-services/our-services.component';
import { ReactiveFormsModule } from '@angular/forms';
import { HttpClientModule } from '@angular/common/http';

@NgModule({
  imports: [
    CommonModule,
    NgbModule,
    QrDesignModule,
    RouterModule,
    ReactiveFormsModule,
    HttpClientModule,
  ],
  declarations: [
    QrBannerComponent,
    QrContentComponent,
    QrHeaderComponent,
    QrLayoutComponent,
    QrFooterComponent,
    QrTrackStormCardComponent,
    QrContactUsFormComponent,
    QrOurServicesCardComponent,
    QrContactUsFormComponent,
  ],
  exports: [
    QrBannerComponent,
    QrContentComponent,
    QrHeaderComponent,
    QrLayoutComponent,
    QrFooterComponent,
    QrTrackStormCardComponent,
    QrContactUsFormComponent,
    QrOurServicesCardComponent,
    QrContactUsFormComponent,
  ],
})
export class QrSharedModule {}
