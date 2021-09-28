declare var google: any;

import { Component, OnInit } from '@angular/core';
import { Store } from '@ngrx/store';
import { distinctUntilChanged, map, take } from 'rxjs/operators';
import { actionStormDataFetchRequest } from '../../store/storm.actions';
import { selectStormData } from '../../store/storm.selectors';
import { GeoJsonLayer } from '@deck.gl/layers';
import { GoogleMapsOverlay } from '@deck.gl/google-maps';
import {
  createDeckInstance,
  destroyDeckInstance,
  getViewState,
} from '../../common/deckgl-utils';

@Component({
  selector: 'qr-storm-map-webgl',
  templateUrl: './qr-storm-map-webgl.component.html',
  styleUrls: ['./qr-storm-map-webgl.component.scss'],
})
export class QrStormMapWebglComponent implements OnInit {
  constructor(private store: Store) {}

  ngOnInit() {
    this.store.dispatch(actionStormDataFetchRequest({ freeMode: false }));
    this.store
      .select(selectStormData)
      .pipe(
        distinctUntilChanged(),
        map((stormData) => {
          if (stormData) {
            console.log('init map');
            this.initMap(stormData.surgeGeoJSON);
          }
        })
      )
      .subscribe((x) => x);
  }

  initMap(data) {
    const div = document.getElementById('map');
    const options = {
      tilt: 0,
      heading: 0,
      center: new google.maps.LatLng(42.4114115, -71.0514695),
      zoom: 3,
      mapId: '11e91ed68dadb48c',
    };

    const map = new google.maps.Map(div, options);

    webglOverlayView.onAdd = () => {};
    webglOverlayView.onContextRestored = (gl) => {};
    webglOverlayView.onDraw = (gl, coordinateTransformer) => {};

    // @ts-ignore TODO(jpoehnelt) fix deckgl typings
    const deckOverlay = new GoogleMapsOverlay({
      useDevicePixels: true,
      layers: [
        // @ts-ignore TODO(jpoehnelt) fix deckgl typings
        new GeoJsonLayer({
          id: 'geojsonm',
          data,
          filled: true,
          pointRadiusMinPixels: 2,
          pointRadiusMaxPixels: 200,
          opacity: 0.4,
          pointRadiusScale: 0.3,
          // getRadius: (f: any) => Math.pow(10, f.properties.mag),
          getFillColor: [255, 70, 30, 180],
          autoHighlight: true,
          // transitions: {
          //   getRadius: {
          //     type: 'spring',
          //     stiffness: 0.1,
          //     damping: 0.15,
          //     enter: (_) => [0], // grow from size 0,
          //     duration: 10000,
          //   },
          // },
          // onDataLoad: (_) => {
          //   // @ts-ignore defined in include
          //   progress.done(); // hides progress bar
          // },
        }),
      ],
    });

    deckOverlay.setMap(map);
  }
}
