import { AgmGeocoder, MapsAPILoader } from '@agm/core';
import {
  Component,
  ElementRef,
  Inject,
  OnInit,
  PLATFORM_ID,
  ViewChild,
} from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';

import { map, take } from 'rxjs/operators';
import { Store } from '@ngrx/store';
import { selectSignUp, selectSignedUser } from '../../store/identity.selectors';
import { QrGeocodingService } from '../../services/geocode.service';
import {
  actionCreateAccountRequest,
  actionSignUpAddressChanged,
} from '../../store/identity.actions';
import { SignUpState, SignedUserState } from '../../store/identity.models';
import { actionUpdateGeolocationRequest } from '../../store/identity.actions';
import { UpdateGeolocationRequestParameters } from '../../models/UpdateGeolocation.models';
import { GeocodedAddress } from '../../models/Geocoding.models';
import { QrGeolocationService } from '../../services/geolocation.service';

@Component({
  selector: 'qr-register-geolocation-page',
  templateUrl: './geolocation.component.html',
  styleUrls: ['./geolocation.component.scss'],
})
export class QrGeolocationPageComponent implements OnInit {
  @ViewChild('mapMarker') googleMapMarker: ElementRef;
  lat: number;
  lng: number;
  formattedAddress: string;
  zoom: number;
  pinMoveAttempts: number;
  infoPopoverVisible: boolean;
  pinAttemptsModalVisible: boolean;
  address: GeocodedAddress;

  constructor(
    private geocodingService: QrGeocodingService,
    private geolocationService: QrGeolocationService,
    private store: Store,
    private router: Router
  ) {}

  $signedUser = this.store.select(selectSignedUser);
  signedUser: SignedUserState;
  $pinDragAttemptsCounter = this.geolocationService.getPinDragAttemptCounter();

  ngOnInit(): void {
    this.zoom = 20;
    this.pinMoveAttempts = 1;
    this.infoPopoverVisible = false;
    this.pinAttemptsModalVisible = false;
    this.$signedUser
      .pipe(
        take(1),
        map((signedUser) => signedUser)
      )
      .subscribe((signedUser) => {
        if (!signedUser) {
          return;
        }
        this.lat = Number(signedUser.user.geolocation.lattitude);
        this.lng = Number(signedUser.user.geolocation.longitude);
        this.formattedAddress = signedUser.user.address.displayText;
        this.address = {
          displayText: signedUser.user.address.displayText,
          city: signedUser.user.address.city,
          state: signedUser.user.address.state,
          streetName: '',
          streetNumber: signedUser.user.address.streetNumber,
          zipCode: signedUser.user.address.zipCode,
          lattitude: signedUser.user.geolocation.lattitude,
          longitude: signedUser.user.geolocation.longitude,
          formattedAddress: signedUser.user.address.displayText,
        };
        this.signedUser = signedUser;
        console.log(signedUser.user);
      });

    this.$pinDragAttemptsCounter
      .pipe(take(1))
      .subscribe((response: { attempt: number }) => {
        if (response.attempt === 5) {
          this.pinMoveAttempts = 5;
          this.pinAttemptsModalVisible = true;
        } else {
          this.pinMoveAttempts = response.attempt + 1;
        }
      });
  }

  onDragEnd(event: any) {
    this.geolocationService
      .incrementPinDragAttemptCounter()
      .subscribe((x) => x);
    if (this.pinMoveAttempts == 5) {
      this.pinAttemptsModalVisible = true;
      this.geolocationService
        .sendPinDragAttemptsExceededEmail()
        .subscribe((x) => x);
      return;
    }

    this.lat = event.latLng.toJSON().lat;
    this.lng = event.latLng.toJSON().lng;

    this.geocodingService
      .geocodeLocation(this.lat, this.lng)
      .pipe(take(1))
      .subscribe((address) => {
        this.address = {
          displayText: address.displayText,
          city: address.city,
          state: address.state,
          streetName: address.streetName,
          streetNumber: address.streetNumber,
          zipCode: address.zipCode,
          lattitude: address.lattitude,
          longitude: address.longitude,
          formattedAddress: address.formattedAddress,
        };
        this.lat = address.lattitude;
        this.lng = address.longitude;
        this.formattedAddress = address.formattedAddress;
      });

    this.pinMoveAttempts = this.pinMoveAttempts.valueOf() + 1;
  }

  onInfoPopoverClose(event) {
    this.infoPopoverVisible = false;
  }

  onGoHomeClick(event) {
    this.router.navigate(['home']);
  }

  onSubmit(event) {
    const params: UpdateGeolocationRequestParameters = {
      address: {
        displayText: this.address.displayText,
        lat: this.address.lattitude,
        lng: this.address.longitude,
      },
      city: this.address.city,
      state: this.address.state,
      street_number:
        this.address.streetName.length === 0
          ? this.address.streetNumber
          : this.address.streetNumber + ' ' + this.address.streetName,
      zip_code: this.address.zipCode,
    };
    this.store.dispatch(
      actionUpdateGeolocationRequest({
        updateGeolocationRequestParameters: params,
      })
    );
  }

  mapReady(map) {
    map.setMapTypeId(google.maps.MapTypeId.HYBRID);
  }
}
