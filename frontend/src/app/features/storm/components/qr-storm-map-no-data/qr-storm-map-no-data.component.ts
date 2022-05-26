import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core';

@Component({
  selector: 'qr-storm-map-no-data',
  templateUrl: './qr-storm-map-no-data.component.html',
  styleUrls: ['./qr-storm-map-no-data.component.scss'],
})
export class QrStormMapNoDataComponent implements OnInit {
  @Input() isStormDataHidden: boolean;
  @Input() zoom: number;
  @Input() restriction: google.maps.MapRestriction;
  @Output() mapHelpClick = new EventEmitter();

  map: any;

  constructor() {}

  ngOnInit() {}

  mapReady(map) {
    this.map = map;

    this.map.setMapTypeId(google.maps.MapTypeId.HYBRID);

    this.map.controls[google.maps.ControlPosition.LEFT_TOP].push(
      document.getElementById('user-data-not-available-message')
    );
  }
  onMapHelpClick($event) {
    this.mapHelpClick.emit();
  }
}
