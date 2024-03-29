import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core';
import { SurgeRiskLevels } from '../../common/constants';

@Component({
  selector: 'qr-storm-map-no-data',
  templateUrl: './qr-storm-map-no-data.component.html',
  styleUrls: ['./qr-storm-map-no-data.component.scss'],
})
export class QrStormMapNoDataComponent implements OnInit {
  @Input() userLattitude: number;
  @Input() userLongitude: number;
  @Input() isStormDataHidden: boolean;
  @Input() noActiveStorm: boolean;
  @Input() isPreprocessed: boolean;
  @Input() zoom: number;
  @Input() restriction: google.maps.MapRestriction;
  @Output() mapHelpClick = new EventEmitter();

  map: any;

  constructor() {}

  get levelsList() {
    return [
      SurgeRiskLevels['N'],
      SurgeRiskLevels['L'],
      SurgeRiskLevels['M'],
      SurgeRiskLevels['H'],
    ];
  }

  ngOnInit() {}

  mapReady(map) {
    this.map = map;

    this.map.setMapTypeId(google.maps.MapTypeId.HYBRID);

    this.map.controls[google.maps.ControlPosition.LEFT_TOP].push(
      document.getElementById('user-data-not-available-message')
    );

    this.map.controls[google.maps.ControlPosition.RIGHT_TOP].push(
      document.getElementById('property-risk')
    );
  }
  onMapHelpClick($event) {
    this.mapHelpClick.emit();
  }
}
