// angular
import { NgModule } from '@angular/core';

// ng-zorro
import { NzLayoutModule } from 'ng-zorro-antd/layout';
import { NzButtonModule } from 'ng-zorro-antd/button';
import { NzImageModule } from 'ng-zorro-antd/image';
import { NzMenuModule } from 'ng-zorro-antd/menu';
import { NzIconModule } from 'ng-zorro-antd/icon';
import { IconDefinition } from '@ant-design/icons-angular';
import { NzCarouselModule } from 'ng-zorro-antd/carousel';
import { NzCardModule } from 'ng-zorro-antd/card';
import { NzGridModule } from 'ng-zorro-antd/grid';
import { NzDividerModule } from 'ng-zorro-antd/divider';
import { NzFormModule } from 'ng-zorro-antd/form';
import { NzInputModule } from 'ng-zorro-antd/input';
import { NzRadioModule } from 'ng-zorro-antd/radio';
import { NzTypographyModule } from 'ng-zorro-antd/typography';
import { NzAlertModule } from 'ng-zorro-antd/alert';
import { NzToolTipModule } from 'ng-zorro-antd/tooltip';
import { NzPopconfirmModule } from 'ng-zorro-antd/popconfirm';
import { NzPopoverModule } from 'ng-zorro-antd/popover';
import { NzModalModule } from 'ng-zorro-antd/modal';
import { NzNotificationModule } from 'ng-zorro-antd/notification';
import { NzSkeletonModule } from 'ng-zorro-antd/skeleton';
import { NzCheckboxModule } from 'ng-zorro-antd/checkbox';
import { NzSwitchModule } from 'ng-zorro-antd/switch';
import { NzProgressModule } from 'ng-zorro-antd/progress';
import { NzSpinModule } from 'ng-zorro-antd/spin';
import { NzSelectModule } from 'ng-zorro-antd/select';
import { NzTableModule } from 'ng-zorro-antd/table';
import { NzSliderModule } from 'ng-zorro-antd/slider';
import { NzSpaceModule } from 'ng-zorro-antd/space';
import { NzDropDownModule } from 'ng-zorro-antd/dropdown';
import { NzDatePickerModule } from 'ng-zorro-antd/date-picker';

import { CreditCardOutline } from '@ant-design/icons-angular/icons';
import { InfoCircleOutline } from '@ant-design/icons-angular/icons';
import { SettingOutline } from '@ant-design/icons-angular/icons';

const icons: IconDefinition[] = [
  CreditCardOutline,
  InfoCircleOutline,
  SettingOutline,
];

import { NZ_I18N } from 'ng-zorro-antd/i18n';
import { en_US } from 'ng-zorro-antd/i18n';

@NgModule({
  exports: [
    // ng-zorro
    NzLayoutModule,
    NzButtonModule,
    NzImageModule,
    NzMenuModule,
    NzIconModule,
    NzCarouselModule,
    NzCardModule,
    NzGridModule,
    NzDividerModule,
    NzFormModule,
    NzInputModule,
    NzRadioModule,
    NzTypographyModule,
    NzAlertModule,
    NzToolTipModule,
    NzPopconfirmModule,
    NzPopoverModule,
    NzNotificationModule,
    NzSkeletonModule,
    NzCheckboxModule,
    NzSwitchModule,
    NzProgressModule,
    NzSpinModule,
    NzModalModule,
    NzSelectModule,
    NzTableModule,
    NzSliderModule,
    NzSpaceModule,
    NzPopconfirmModule,
    NzDropDownModule,
    NzDatePickerModule,
  ],
  imports: [NzIconModule.forRoot(icons)],
  providers: [{ provide: NZ_I18N, useValue: en_US }],
})
export class QrDesignModule {}
