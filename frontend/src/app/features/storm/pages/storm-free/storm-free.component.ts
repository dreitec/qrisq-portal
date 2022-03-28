import {Component, OnInit} from '@angular/core';
import {Router} from '@angular/router';
import {Store} from '@ngrx/store';
import {StormData} from '../../models/storm.models';
import {DomSanitizer} from '@angular/platform-browser';
import {environment} from '@env';
import * as AWS from 'aws-sdk';


@Component({
  selector: 'qr-storm-free-page',
  templateUrl: './storm-free.component.html',
  styleUrls: ['./storm-free.component.scss'],
})
export class QrStormFreePageComponent implements OnInit {
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
  identityPoolId: string = environment.COGNITO_IDENTITY_POOL;
  stormData: StormData;
  stormName: string;
  stormAdv: string;

  userGeolocation: {
    lattitude: number;
    longitude: number;
    address: string;
  };

  constructor(private store: Store, private router: Router, private sanitizer: DomSanitizer) {}

  ngOnInit() {
    AWS.config.region = 'us-east-1';
    AWS.config.credentials = new AWS.CognitoIdentityCredentials({
      IdentityPoolId: this.identityPoolId
    });
    this.getStormData();
    // this.store.dispatch(actionStormDataFetchRequest({ freeMode: true }));

    // this.store.select(selectStormData).subscribe((stormData) => {
    //   if (stormData) {
    //     console.log(stormData);
    //     this.stormData = stormData;
    //     this.isDataLoaded = true;
    //     this.getStormData();
    //     this.stormName = storm_name;
    //     // this.stormAdv = adv_date_parsed;
    //   }
    // });
  }

  getStormData() {
    AWS.config.region = 'us-east-1';
    AWS.config.credentials = new AWS.CognitoIdentityCredentials({
      IdentityPoolId: this.identityPoolId
    });
    var lambda = new AWS.Lambda();
    var input;
    input = { utc: 'None' };
    lambda.invoke(
      {
        FunctionName: 'aws-lambda-point',
        Payload: JSON.stringify(input),
      },
      (err, data: any) => {
        if (err) {
          console.log(err, err.stack);
        } else {
          var data_decode = atob(data.Payload);
          var data_bin_gzd = pako.inflate(data_decode);
          var data_str = new TextDecoder('utf-8').decode(data_bin_gzd);
          var geojson_obj = JSON.parse(data_str);
          var storm_name =
            geojson_obj['features'][0]['properties']['STORMNAME'];
          storm_name = storm_name.trim();
          var adv_num = geojson_obj['features'][0]['properties']['ADVISNUM'];
          var advisory_heading = 'Forecast Advisory: #' + adv_num.trim();
          var adv_date = geojson_obj['features'][0]['properties']['ADVDATE'];
          var adv_date_parsed = adv_date.split(' ');
          var advisory_date =
            adv_date_parsed[4] +
            ' ' +
            adv_date_parsed[5] +
            ', ' +
            adv_date_parsed[6] +
            ' @ ' +
            adv_date_parsed[0].substring(0, adv_date_parsed[0].length - 2) +
            ':' +
            adv_date_parsed[0].substring(adv_date_parsed[0].length - 2) +
            ' ' +
            adv_date_parsed[1] +
            ' ' +
            adv_date_parsed[2];
          this.stormName = storm_name;
          this.stormAdv = advisory_date;
          //       // var live_storm_header_div = document.createElement('div');
          //       // live_storm_header_div.id = 'header_div_id';
          //       // live_storm_header_div.style.width = '100%';
          //       // live_storm_header_div.style.height = '75px';
          //       // live_storm_header_div.style.padding = '0px 0px 0px 0px';
          //       // live_storm_header_div.style.margin = '0px auto 0px auto';
          //       // live_storm_header_div.style.backgroundColor = '#222222';
          //       // live_storm_header_div.style.color = 'white';
          //       // live_storm_header_div.style.zIndex = '0';
          //       // live_storm_header_div.className =
          //       //   'container clearfix et_menu_container';
          //       // live_storm_header_div.innerHTML =
          //       //   '<h1 style="color: white;">' +
          //       //   storm_name +
          //       //   '</h1>&nbsp' +
          //       //   advisory_date;
          //       // button_container_div_element.appendChild(live_storm_header_div);
        }
      }
    );
  }

  onMapHelpClick() {
    this.router.navigate(['contact-us']);
  }

  onMapModeChange(mode) {
    console.log(mode);
    this.mapMode = mode;
  }

  onMapLoaded(event) {}

  onTrackAndConeChanged(trackAndCone) {
    this.isTrackAndConeChecked = trackAndCone;
  }
}
