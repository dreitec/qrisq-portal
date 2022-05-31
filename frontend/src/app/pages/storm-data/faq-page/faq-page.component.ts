import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'qr-faq-page',
  templateUrl: './faq-page.component.html',
  styleUrls: ['./faq-page.component.scss'],
})
export class QrFaqPageComponent implements OnInit {
  constructor() {}

  activeList = [];

  ngOnInit(): void {}

  onActiveChange(active, name) {
    if (active) {
      this.activeList.push(name);
    } else {
      this.activeList = this.activeList.filter(v => v !== name);
    }
  }
}
