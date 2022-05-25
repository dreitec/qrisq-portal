/* tslint:disable: variable-name */
import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core';
import { GoogleMapsOverlay } from '@deck.gl/google-maps';
import { GeoJsonLayer } from '@deck.gl/layers';
import {
  SurgeRiskLevels,
  StormMarkerIcons,
  WindRiskLevels,
} from '../../common/constants';
import moment from 'moment';
import { Observable } from 'rxjs';
import hexRgb from 'hex-rgb';
import { getESRISurgeLevelColor } from '../../common/utils';
import { HurricaneIconSVG } from '../../common/svg';

@Component({
  selector: 'qr-storm-map',
  templateUrl: './qr-storm-map.component.html',
  styleUrls: ['./qr-storm-map.component.scss'],
})
export class QrStormMapComponent implements OnInit {
  @Input() isStormDataHidden: boolean;
  @Input() surgeGeoJSON: any;
  @Input() lineGeoJSON: Object;
  @Input() pointsGeoJSON: any;
  @Input() polygonsGeoJSON: Object;
  @Input() windGeoJSON: Object;
  @Input() windData: any;
  @Input() userLattitude: number;
  @Input() userLongitude: number;
  @Input() surgeRisk: string;
  @Input() windRisk: string;
  @Input() stormDistance: number;
  @Input() centerStormIcon: string;
  @Input() mode: string;
  @Input() zoom: number;
  @Input() restriction: google.maps.MapRestriction;
  @Input() freeMode: boolean;
  @Input() userDataAvailable: boolean;
  @Output() modeChange = new EventEmitter<string>();
  @Output() trackAndConeChanged = new EventEmitter<boolean>();
  @Output() mapLoaded = new EventEmitter<boolean>();
  @Output() mapHelpClick = new EventEmitter();

  map: any;
  canvasLayer: any;
  infowindow = new google.maps.InfoWindow();
  timer: any;
  stormLattitude = 0;
  stormLongitude = 0;
  // tslint:disable-next-line: variable-name
  _activeLayer = 'surge';
  isSettingsVisible = false;
  windy = null;
  boundsChangedLister = null;
  vortexConfig = {
    velocityScale: 0.01,
    intensityScaleStep: 30,
    maxWindIntensity: 50,
    maxParticleAge: 4,
    particleLineWidth: 0.5,
    particleMultiplier: 30,
    particleReduction: 50,
    frameRate: 30,
  };

  stormDistanceLabel = null;

  context: any;

  private lineGeoJsonFeatures: any;
  private pointsGeoJsonFeatures: any;
  private polygonsGeoJsonFeatures: any;
  private surgeGeoJsonFeatures: any;
  private _windGeoJSON: any;

  // tslint:disable-next-line: variable-name
  private _isTrackAndConeChecked = true;

  public get isTrackAndConeChecked(): boolean {
    return this._isTrackAndConeChecked;
  }

  public set isTrackAndConeChecked(value: boolean) {
    if (value) {
      if (this.stormDistanceLabel) {
        this.stormDistanceLabel.show();
      }
      this.showLineGeoJsonLayer();
      this.showPointsGeoJsonLayer();
      this.showPolygonsGeoJsonLayer();
    } else {
      if (this.stormDistanceLabel) {
        this.stormDistanceLabel.hide();
      }
      this.hideLineGeoJsonLayer();
      this.hidePointsGeoJsonLayer();
      this.hidePolygonsGeoJsonLayer();
    }

    this.trackAndConeChanged.emit(value);
    this._isTrackAndConeChecked = value;
  }

  public get activeLayer(): string {
    return this._activeLayer;
  }

  public set activeLayer(v: string) {
    if (v === 'surge') {
      this.modeChange.emit('surge');
      this.canvasLayer.setMap(null);
      this.showSurgeGeoJsonLayer();
    } else if (v === 'wind') {
      this.modeChange.emit('wind');
      this.canvasLayer.setMap(null);
      this.hideSurgeGeoJsonLayer();
    } else {
      this.modeChange.emit('vortex');
      this.isTrackAndConeChecked = false;
      this.canvasLayer.setMap(this.map);
      this.hideSurgeGeoJsonLayer();
    }
    this._activeLayer = v;
  }

  get levels() {
    return SurgeRiskLevels;
  }

  get categories() {
    return WindRiskLevels;
  }

  get levelsList() {
    return [
      SurgeRiskLevels['N'],
      SurgeRiskLevels['L'],
      SurgeRiskLevels['M'],
      SurgeRiskLevels['H'],
    ];
  }

  get categoriesList() {
    return [
      WindRiskLevels['N'],
      WindRiskLevels['TS'],
      WindRiskLevels['1'],
      WindRiskLevels['2'],
      WindRiskLevels['3'],
      WindRiskLevels['4'],
      WindRiskLevels['5'],
    ];
  }

  isChecked = true;

  constructor() {}

  ngOnInit() {}

  getUserLocationIcon(surgeRisk) {
    return {
      path:
        'm503.898438 231.476562-236.800782-226.984374c-6.1875-5.976563-16-5.976563-22.1875 0l-237.011718 227.199218c-5.121094 4.90625-7.89453175 11.945313-7.89453175 18.984375 0 14.722657 11.94921875 26.667969 26.66796875 26.667969h37.332031v192c0 23.46875 19.203125 42.667969 42.667969 42.667969h298.667969c23.464844 0 42.664062-19.199219 42.664062-42.667969v-192h37.335938c14.71875 0 26.664062-11.945312 26.664062-26.667969 0-7.039062-2.773437-14.078125-8.105468-19.199219zm0 0',
      fillColor: this.levels[surgeRisk].colorHex,
      fillOpacity: 1,
      strokeWeight: 1,
      rotation: 0,
      scale: 2,
      anchor: new google.maps.Point(this.userLattitude, this.userLongitude),
    };
  }

  trackByFeatureId(index, feature) {
    return feature.properties.id;
  }

  getMarkerIconUrl(iconId) {
    return StormMarkerIcons[iconId];
  }

  onSurgeLayerClick(event) {
    var feat = event.feature;
    // const poly = polygon([feat.geometry.coordinates[0]]);
    // const center = centerOfMass(polygon);
    // console.log(center);
    const maxft = Number(Number(feat.getProperty('maxft')).toFixed(2));
    const eleavg = Number(Number(feat.getProperty('eleavg')).toFixed(2));
    const elemax = Number(Number(feat.getProperty('elemax')).toFixed(2));
    const elemin = Number(Number(feat.getProperty('elemin')).toFixed(2));
    let html = `<b>Max Depth:</b> ${maxft} ft.<br />`;
    html += `<b>Elev. Avg.:</b> ${eleavg}<br />`;
    html += `<b>Elev. Max.:</b> ${elemax}<br />`;
    html += `<b>Elev. Min.:</b> ${elemin}`;
    this.infowindow.setContent(html);
    this.infowindow.setPosition(event.latLng);
    this.infowindow.open(this.map);
  }

  setSurgeGeoJsonStyle() {
    this.surgeGeoJsonFeatures.forEach((feature) => {
      const style = feature.getProperty('style');
      this.map.data.overrideStyle(feature, style);
    });
  }

  showSurgeGeoJsonLayer() {
    this.surgeGeoJsonFeatures.forEach((feature) => {
      const style = feature.getProperty('style');
      style.visible = true;
      this.map.data.overrideStyle(feature, style);
    });
  }

  hideSurgeGeoJsonLayer() {
    this.surgeGeoJsonFeatures.forEach((feature) => {
      const style = feature.getProperty('style');
      style.visible = false;
      this.map.data.overrideStyle(feature, style);
    });
  }

  setLineGeoJsonStyle() {
    this.lineGeoJsonFeatures.forEach((feature) => {
      const style = feature.getProperty('style');
      this.map.data.overrideStyle(feature, style);
    });
  }

  showLineGeoJsonLayer() {
    this.lineGeoJsonFeatures.forEach((feature) => {
      const style = feature.getProperty('style');
      style.visible = true;
      this.map.data.overrideStyle(feature, style);
    });
  }

  hideLineGeoJsonLayer() {
    this.lineGeoJsonFeatures.forEach((feature) => {
      const style = feature.getProperty('style');
      style.visible = false;
      this.map.data.overrideStyle(feature, style);
    });
  }

  setPointsGeoJsonStyle() {
    this.pointsGeoJsonFeatures.forEach((feature) => {
      const style = feature.getProperty('style');
      this.map.data.overrideStyle(feature, style);
    });
  }

  showPointsGeoJsonLayer() {
    this.pointsGeoJsonFeatures.forEach((feature) => {
      const style = feature.getProperty('style');
      style.visible = true;
      this.map.data.overrideStyle(feature, style);
    });
  }

  hidePointsGeoJsonLayer() {
    this.pointsGeoJsonFeatures.forEach((feature) => {
      const style = feature.getProperty('style');
      style.visible = false;
      this.map.data.overrideStyle(feature, style);
    });
  }

  setPolygonsGeoJsonStyle() {
    this.polygonsGeoJsonFeatures.forEach((feature) => {
      const style = feature.getProperty('style');
      this.map.data.overrideStyle(feature, style);
    });
  }

  showPolygonsGeoJsonLayer() {
    this.polygonsGeoJsonFeatures.forEach((feature) => {
      const style = feature.getProperty('style');
      style.visible = true;
      this.map.data.overrideStyle(feature, style);
    });
  }

  hidePolygonsGeoJsonLayer() {
    this.polygonsGeoJsonFeatures.forEach((feature) => {
      const style = feature.getProperty('style');
      style.visible = false;
      this.map.data.overrideStyle(feature, style);
    });
  }

  windStyleFunc(feature) {
    return {
      clickable: feature.getProperty('clickable'),
      cursor: feature.getProperty('cursor'),
      draggable: feature.getProperty('draggable'),
      editable: feature.getProperty('editable'),
      fillColor: feature.getProperty('fill'),
      fillOpacity: 0.8,
      strokeColor: feature.getProperty('fill'),
      strokeOpacity: 0.8,
      strokeWeight: 0.6,
      title: feature.getProperty('title'),
      visible: feature.getProperty('visible'),
      zIndex: feature.getProperty('zIndex'),
      icon: feature.getProperty('icon'),
    };
  }

  surgeStyleFunc(feature) {
    const maxft = feature.getProperty('maxft');
    let fillColor = '#fff';
    fillColor = getESRISurgeLevelColor(Number.parseFloat(maxft));
    return {
      clickable: false,
      draggable: false,
      editable: false,
      fillColor: fillColor,
      fillOpacity: 0.7,
      strokeColor: fillColor,
      strokeWeight: 0.3,
      strokeOpacity: 0.75,
      visible: feature.getProperty('visible'),
    };
  }

  mapReadyNoData(map) {
    this.mapLoaded.emit(true);
    this.map = map;
    this.map.setMapTypeId(google.maps.MapTypeId.HYBRID);
    this.map.controls[google.maps.ControlPosition.LEFT_TOP].push(
      document.getElementById('user-data-not-available-message')
    );
  }

  mapReady(map) {
    this.mapLoaded.emit(true);
    this.map = map;

    const points = this.pointsGeoJSON.features;
    this.stormLattitude = points[0].geometry.coordinates[1];
    this.stormLongitude = points[0].geometry.coordinates[0];

    // const geojsonLayer = new GeoJsonLayer({
    //   id: 'geojsonLayer',
    //   data: this.surgeGeoJSON,
    //   pickable: false,
    //   // pointRadiusMinPixels: 2,
    //   // pointRadiusMaxPixels: 140,
    //   // wrapLongitude: true,
    //   // getRadius: d => d.properties.capacity * 40,
    //   // getLineColor: (d) => {
    //   //   const rgb = hexRgb(
    //   //     getESRISurgeLevelColor(Number.parseFloat(d.properties.maxft))
    //   //   );

    //   //   return [rgb.red, rgb.green, rgb.blue, 130];
    //   // },
    //   // getFillColor: (d) => {
    //   //   const rgb = hexRgb(
    //   //     getESRISurgeLevelColor(Number.parseFloat(d.properties.maxft))
    //   //   );

    //   //   return [rgb.red, rgb.green, rgb.blue, 130];
    //   // },
    // });
    // const overlay = new GoogleMapsOverlay({
    //   layers: [geojsonLayer],
    // });
    // overlay.setMap(map);

    this.map.setMapTypeId(google.maps.MapTypeId.HYBRID);

    this.map.controls[google.maps.ControlPosition.LEFT_BOTTOM].push(
      document.getElementById('select-map-layer')
    );

    this.map.controls[google.maps.ControlPosition.RIGHT_TOP].push(
      document.getElementById('property-risk')
    );

    this.map.controls[google.maps.ControlPosition.RIGHT_BOTTOM].push(
      document.getElementById('legend-water-depth')
    );

    // this.map.controls[google.maps.ControlPosition.LEFT_TOP].push(
    //   document.getElementById('user-data-not-available-message')
    // );
    // this.map.controls[google.maps.ControlPosition.LEFT_TOP].push(
    //   document.getElementById('map-settings')
    // );

    if (!this.freeMode) {
      if (this.userDataAvailable) {
        const b = new google.maps.LatLngBounds();
        b.extend(
          new google.maps.LatLng(this.userLattitude, this.userLongitude)
        );
        b.extend(
          new google.maps.LatLng(this.stormLattitude, this.stormLongitude)
        );
        this.stormDistanceLabel = new ELabel({
          latlng: new google.maps.LatLng(
            b.getCenter().lat(),
            b.getCenter().lng()
          ),
          label: this.stormDistance.toString() + ' Miles',
          classname: 'distance-label',
        });
        this.stormDistanceLabel.setMap(map);
      }
    }

    // marker.setMap(map);
    let timer;
    const canvasLayerOptions = {
      map: map,
      animate: false,
      updateHandler: (overlay, params) => {
        if (timer) {
          window.clearTimeout(timer);
        }

        timer = setTimeout(() => {
          const bounds = map.getBounds();
          const mapSizeX = map.getDiv().offsetWidth;
          const mapSizeY = map.getDiv().offsetHeight;
          this.windy.start(
            [
              [0, 0],
              [mapSizeX, mapSizeY],
            ],
            mapSizeX,
            mapSizeY,
            [
              [bounds.getSouthWest().lng(), bounds.getSouthWest().lat()],
              [bounds.getNorthEast().lng(), bounds.getNorthEast().lat()],
            ]
          );
        }, 750);
      },
    };

    this.canvasLayer = new CanvasLayer(canvasLayerOptions);
    this.canvasLayer.setMap(null);

    this.windy = Windy({
      canvas: this.canvasLayer.canvas,
      data: this.windData,
      vortexConfig: this.vortexConfig,
    });

    //prepare context var
    this.context = this.canvasLayer.canvas.getContext('2d');

    this.boundsChangedLister = google.maps.event.addListener(
      map,
      'bounds_changed',
      () => {
        this.windy.stop();
        this.context.clearRect(0, 0, 3000, 3000);
      }
    );

    //clear canvas and stop animation
    function clearWind() {
      this.windy.stop();
      this.context.clearRect(0, 0, 3000, 3000);
    }

    // map.on('dragstart', function () {
    //   clearWind();
    // });
    // map.on('zoomstart', function () {
    //   clearWind();
    // });
    // map.on('resize', function () {
    //   clearWind();
    // });

    this.lineGeoJsonFeatures = this.map.data.addGeoJson(this.lineGeoJSON);
    this.setLineGeoJsonStyle();
    this.showLineGeoJsonLayer();

    this.pointsGeoJsonFeatures = this.map.data.addGeoJson(this.pointsGeoJSON);
    this.setPointsGeoJsonStyle();
    this.showPointsGeoJsonLayer();

    this.polygonsGeoJsonFeatures = this.map.data.addGeoJson(
      this.polygonsGeoJSON
    );
    this.setPolygonsGeoJsonStyle();
    this.showPolygonsGeoJsonLayer();

    this.surgeGeoJsonFeatures = this.map.data.addGeoJson(this.surgeGeoJSON);
    this.setSurgeGeoJsonStyle();
    this.showSurgeGeoJsonLayer();
  }

  onClearReact(event) {
    this.canvasLayer.setMap(null);
    this.canvasLayer.setMap(this.map);
  }

  sortByForecastLongDate(fa, fb) {
    const dateFormat = 'YYYY-M-D h:mm A ddd [CDT]';
    const propName = 'FLDATELBL';
    const d1 = moment(fa.properties[propName], dateFormat);
    const d2 = moment(fb.properties[propName], dateFormat);
    if (d1.isAfter(d2)) {
      return 1;
    }
    if (d1.isBefore(d2)) {
      return -1;
    }
    return 0;
  }

  getMarkerPoints(featureCollection) {
    const points: Array<any> = featureCollection.features;

    const sortedPoints = points.slice().sort(this.sortByForecastLongDate);
    this.stormLattitude = Number.parseFloat(sortedPoints[0].properties['LAT']);
    this.stormLongitude = Number.parseFloat(sortedPoints[0].properties['LON']);
    // console.log(Number.parseFloat(sortedPoints[0].properties['LAT']));
    // console.log(Number.parseFloat(sortedPoints[0].properties['LON']));

    const markers = [];
    for (let i = 0; i < sortedPoints.length; i++) {
      const circle: google.maps.Symbol = {
        path: google.maps.SymbolPath.CIRCLE,
        scale: 7,
      };
      let marker = {
        lattitude: Number.parseFloat(sortedPoints[0].properties['LAT']),
        longitude: Number.parseFloat(sortedPoints[0].properties['LON']),
        iconUrl: circle,
        label: '',
      };
      markers.push(marker);
    }
    // console.log(featureCollection);
    return markers;
  }

  onSettingsSubmit($event) {
    this.isSettingsVisible = false;
  }
  onSettingsCancel($event) {
    this.isSettingsVisible = false;
  }
  onMapHelpClick($event) {
    this.mapHelpClick.emit();
  }
}
