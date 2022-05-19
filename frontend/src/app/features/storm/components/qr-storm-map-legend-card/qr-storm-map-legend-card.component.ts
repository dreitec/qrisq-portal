import { Component, Input, OnInit } from '@angular/core';

@Component({
  selector: 'qr-storm-map-legend-card',
  templateUrl: './qr-storm-map-legend-card.component.html',
  styleUrls: ['./qr-storm-map-legend-card.component.scss'],
})
export class QrStormMapLegendCardComponent implements OnInit {
  @Input() title: string;

  constructor() {}

  isCollapsed = true;

  ngOnInit() {}

  onCollapsed() {
    this.isCollapsed = !this.isCollapsed;
  }

}
