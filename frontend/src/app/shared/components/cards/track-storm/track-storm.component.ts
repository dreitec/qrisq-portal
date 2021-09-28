import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'qr-track-storm-card',
  templateUrl: './track-storm.component.html',
  styleUrls: ['./track-storm.component.scss'],
})
export class QrTrackStormCardComponent implements OnInit {
  constructor(private router: Router) {}

  ngOnInit() {}

  onGoToPageClick(event) {
    window.open('https://www.nhc.noaa.gov/', '_blank');
  }
}
