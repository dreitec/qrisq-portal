// angular
import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { QrContactUsService } from './services/contact-us.service';
import { QrDesignModule } from '@app/design/design.module';
import { QrSharedModule } from '@app/shared/shared.module';
import { QrCoreModule } from '@app/core/core.module';
import { HttpClientModule } from '@angular/common/http';
import { QrContactUsPageComponent } from './pages/contact-us/contact-us.component';

@NgModule({
  declarations: [QrContactUsPageComponent],
  imports: [
    // angular
    CommonModule,
    ReactiveFormsModule,
    HttpClientModule,
    FormsModule,

    // modules
    QrDesignModule,
    QrSharedModule,
    QrCoreModule,
  ],
  providers: [QrContactUsService],
  exports: [QrContactUsPageComponent],
})
export class QrContactUsModule {}
