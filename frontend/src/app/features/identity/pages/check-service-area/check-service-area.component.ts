// angular
import { Component, OnInit, ViewChild } from '@angular/core';

// google maps
import { GooglePlaceDirective } from 'ngx-google-places-autocomplete';
import { Address } from 'ngx-google-places-autocomplete/objects/address';

// rxjs
import { map, take, takeLast } from 'rxjs/operators';

// ngrx
import { Store } from '@ngrx/store';

// store
import { actionCheckServiceAreaRequest } from '../../store/identity.actions';

// component store
import { QrCheckServiceAreaComponentStore } from './check-service-area.component-store';
import { Observable } from 'rxjs';

@Component({
  selector: 'qr-check-service-area',
  templateUrl: './check-service-area.component.html',
  styleUrls: ['./check-service-area.component.scss'],
})
export class QrCheckServiceAreaPageComponent implements OnInit {
  constructor(
    private componentStore: QrCheckServiceAreaComponentStore,
    private store: Store
  ) {}

  @ViewChild('placesRef') placesRef: GooglePlaceDirective;

  isLocation$ = this.componentStore.IsLocation$;

  location$ = this.componentStore.state$.subscribe((state) => {
    this.location = {
      lattitude: state.lattitude,
      longitude: state.longitude,
    };
  });

  location: {
    lattitude: number | null;
    longitude: number | null;
  } = {
    lattitude: 0,
    longitude: 0,
  };

  ngOnInit(): void {
    this.componentStore.resetState();
  }

  public onAddressChange(address: Address): void {
    const lattitude = address.geometry.location.lat();
    const longitude = address.geometry.location.lng();
    this.componentStore.updateLocation({ lattitude, longitude });
  }

  public OnSearch(): void {
    this.store.dispatch(actionCheckServiceAreaRequest(this.location));
    this.location$.unsubscribe();
  }
}
