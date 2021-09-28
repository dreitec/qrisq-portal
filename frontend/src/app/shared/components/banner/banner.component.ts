import { Component, Input, OnInit } from '@angular/core';

@Component({
  selector: 'qr-banner',
  templateUrl: './banner.component.html',
  styleUrls: ['./banner.component.scss'],
})
export class QrBannerComponent implements OnInit {
  @Input() imageUrl: string; // decorate the property with @Input()

  constructor() {}

  ngOnInit() {}
}
