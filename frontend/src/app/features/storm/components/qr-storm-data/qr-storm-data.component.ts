import { Component, Input, OnInit } from '@angular/core';
import { WindRiskLevels, SurgeRiskLevels } from '../../common/constants';
import { TimeUtils } from '../../common/utils';
import round from 'round';

@Component({
  selector: 'qr-storm-data',
  templateUrl: './qr-storm-data.component.html',
  styleUrls: ['./qr-storm-data.component.scss'],
})
export class QrStormDataComponent implements OnInit {
  @Input() mode: string;
  @Input() stormName: string;
  @Input() userAddress: string;
  @Input() surgeRisk: string;
  @Input() windRisk: string;
  @Input() advisoryDate: string;
  @Input() windAdvisoryDate: string;
  @Input() floodAdvisoryDate: string;
  @Input() landfallDate: Date;
  @Input() landfallLocation: string;
  @Input() stormDistance: number;
  @Input() forecastAdvisory: number;
  @Input() nextAdvisoryDate: number;
  @Input() userDataAvailable: boolean;
  @Input() isTrackAndConeChecked: boolean;
  @Input() noActiveStorm: boolean;
  @Input() maxFlood: number;

  public get windLevels() {
    return WindRiskLevels;
  }

  public get surgeLevels() {
    return SurgeRiskLevels;
  }

  constructor() {}

  ngOnInit() {}

  toCDT(date) {
    return TimeUtils.toCDT(date);
  }

  toFeet(meters: number) {
    return round(meters * 3.281, 0.5);
  }
}
