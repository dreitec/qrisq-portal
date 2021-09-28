import {
  Component,
  EventEmitter,
  HostListener,
  Input,
  OnInit,
  Output,
} from '@angular/core';
import { Router } from '@angular/router';
import { Store } from '@ngrx/store';

@Component({
  selector: 'qr-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.scss'],
})
export class QrHeaderComponent implements OnInit {
  public isMenuCollapsed = true;
  @Input() isUserLogin: boolean;
  @Input() userFirstName: string;
  @Input() isAdmin: boolean;
  @Output() logout = new EventEmitter<Event>();

  constructor(private router: Router, private store: Store) {}

  ngOnInit(): void {}

  // tslint:disable-next-line: prefer-inline-decorator
  @HostListener('window:scroll', ['$event'])
  onWindowScroll(e) {
    let element = document.querySelector('.navbar');
    if (window.pageYOffset > element.clientHeight) {
      element.classList.add('navbar-dark');
    } else {
      element.classList.remove('navbar-dark');
    }
  }

  openStormViewer() {
    if (this.isUserLogin) {
      this.router.navigate(['/storm']);
    } else {
      this.router.navigate(['/storm-free']);
    }
  }

  onLogout($event) {
    this.logout.emit($event);
  }
}
