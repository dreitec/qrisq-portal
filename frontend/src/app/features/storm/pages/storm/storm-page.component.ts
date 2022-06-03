import { HttpClient } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import { environment } from '@env';
import { Store } from '@ngrx/store';
import { Observable } from 'rxjs';

import { WindRiskLevels } from '../../common/constants';
import { TimeUtils } from '../../common/utils';
import { actionStormDataFetchRequest } from '../../store/storm.actions';
import { selectStormData } from '../../store/storm.selectors';

import { QrStormService } from '../../services/storm.service';
import { QrIdentityService } from '@app/features/identity/services/identity.service';
import { selectSignedUser } from '@app/features/identity/store/identity.selectors';
import { filter, map, take } from 'rxjs/operators';
import { StormData } from '../../models/storm.models';
import { actionSignInRequest } from '@app/features/identity/store/identity.actions';
import { selectIdentityState } from '../../../identity/store/identity.selectors';
import { NavigationEnd, Router } from '@angular/router';

@Component({
  selector: 'qr-storm-page',
  templateUrl: './storm-page.component.html',
  styleUrls: ['./storm-page.component.scss'],
})
export class QrStormPageComponent implements OnInit {
  mapMode = 'surge';
  isTrackAndConeChecked = true;
  loadingMap = true;
  mapZoom = 4;
  mapRestriction: google.maps.MapRestriction = {
    latLngBounds: {
      north: 60,
      south: 5,
      west: -120,
      east: -30,
    },
    strictBounds: true,
  };
  isDataLoaded = false;
  isStormDataHidden = false;
  isMapPage = true;

  stormData: any;
  userDataAvailable: boolean;

  userGeolocation: {
    lattitude: number;
    longitude: number;
    address: string;
  };

  constructor(
    private store: Store,
    private router: Router,
    private identityService: QrIdentityService,
    private stormService: QrStormService
  ) {
    router.events.subscribe((val) => {
      if (val instanceof NavigationEnd) {
        if (val.url.includes('/storm/')) {
          this.isMapPage = false;
        } else {
          this.isMapPage = true;
        }
      }
    });
  }

  ngOnInit() {
    this.isDataLoaded = true;
    this.stormData = null;
    this.userDataAvailable = false;
    this.isDataLoaded = false;
    this.store
      .select(selectSignedUser)
      .pipe(
        take(1),
        map((signedUser) => ({
          lattitude: signedUser.user.geolocation.lattitude,
          longitude: signedUser.user.geolocation.longitude,
          address: signedUser.user.address.displayText,
        }))
      )
      .subscribe((userGeolocation) => {
        this.userGeolocation = userGeolocation;
        this.loadStormData();
      });

    this.store.select(selectStormData).subscribe((stormData) => {
      if (stormData) {
        this.stormData = stormData;
        this.isDataLoaded = true;
      }
    });
  }

  loadStormData(refresh?: boolean) {
    if (!refresh) {
      this.isDataLoaded = false;
    }
    this.stormService
      .getStormData(false)
      .pipe(take(1))
      .subscribe((stormData) => {
        this.userDataAvailable = stormData.userDataAvailable;
        this.stormData = stormData;
        this.isDataLoaded = true;

        if (!stormData?.isPreprocessed || stormData?.noActiveStorm) {
          setTimeout(() => this.loadStormData(true), 15000);
        }
      });
  }

  onMapHelpClick() {
    this.router.navigate(['contact-us']);
  }

  onMapModeChange(mode) {
    this.mapMode = mode;
  }

  onMapLoaded(event) {}

  onTrackAndConeChanged(trackAndCone) {
    this.isTrackAndConeChecked = trackAndCone;
  }

  onStormDataHidden() {
    this.isStormDataHidden = !this.isStormDataHidden;
  }
}
