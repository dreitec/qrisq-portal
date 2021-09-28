import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'qr-our-services-card',
  templateUrl: './our-services.component.html',
  styleUrls: ['./our-services.component.scss'],
})
export class QrOurServicesCardComponent implements OnInit {
  constructor(private router: Router) {}

  ngOnInit() {}

  onGoToServicesClick(event) {
    this.router.navigate(['services', 'homeowners']);
  }
}
