import { Component } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'qr-admin-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.scss'],
})
export class QrAdminDashboardComponent {
  constructor(private router: Router) {}

  ngOnInit(): void {
    this.router.navigate(['/admin/administrators']);
  }
}
