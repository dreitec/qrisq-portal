import { Component, Input, OnInit } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'qr-footer',
  templateUrl: './footer.component.html',
  styleUrls: ['./footer.component.scss'],
})
export class QrFooterComponent implements OnInit {
  @Input() isAuthenticated: boolean;

  constructor(private router: Router) {}

  ngOnInit(): void {}
}
