import { Component, Input, OnInit } from '@angular/core';
import { WindRiskLevels, SurgeRiskLevels } from '../../common/constants';
import { getWindDirection, TimeUtils } from '../../common/utils';
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
  @Input() issuedDate: string;
  @Input() stormAdvisoryLatitude: number;
  @Input() stormAdvisoryLongitude: number;
  @Input() stormAdvisoryDirection: string;
  @Input() stormAdvisorySpeed: number;
  @Input() stormAdvisoryWind: number;
  @Input() stormAdvisoryPressure: number;
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

  toIssuedDate(date) {
    return TimeUtils.toIssuedDate(date);
  }

  getAdvisoryLocation() {
    return `${this.stormAdvisoryLatitude.toFixed(1)} N, ${Math.abs(this.stormAdvisoryLongitude).toFixed(1)} W`;
  }

  getWindDirection(degree) {
    return getWindDirection(degree);
  }

  convertKnot2MPH(value) {
    return (value * 1.151).toFixed(1);
  }

  getWindSpeedWholeNumber(value) {
    return parseInt(`${value * 1.151}`);
  }

  toFeet(meters: number) {
    return round(meters * 3.281, 0.5);
  }
}
