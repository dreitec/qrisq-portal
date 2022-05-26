import { HttpClient, HttpParams, HttpResponse } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { forkJoin, Observable, of } from 'rxjs';
import { catchError, map, switchMap, take, tap } from 'rxjs/operators';

import moment from 'moment';
import pako from 'pako';

import { environment } from '@env';
import { StormData } from '../models/storm.models';
import { getESRISurgeLevelColor } from '../common/utils';
import { StormMarkerIcons } from '../common/constants';

@Injectable({
  providedIn: 'root',
})
export class QrStormService {
  constructor(private httpClient: HttpClient) {}

  getStormData(freeMode: boolean): Observable<StormData> {
    return new Observable<StormData>((observer) => {
      forkJoin({
        storm: this.getStormParameters(freeMode),
        surge: this.getSurgeParameters(),
        wind: this.getWindParameters(),
      })
        .pipe(
          catchError((err) => {
            console.log('caught rethrown error, providing fallback value');
            return of(null);
          })
        )
        .subscribe((result) => {
          if (!result || (Object.keys(result.storm).length < 1)) {
            const stormData: StormData = {
              lattitude: 0,
              longitude: 0,
              address: '',
              clientId: 0,
              surgeRisk: '',
              maxFlood: 0,
              forecastAdvisory: 0,
              advisoryDate: '',
              floodAdvisoryDate: '',
              windAdvisoryDate: '',
              floodNextAdvisoryDate: '',
              windNextAdvisoryDate: '',
              nextAdvisoryDate: '',
              landfallDate: null,
              landfallLocation: '',
              stormDistance: 0,
              stormName: '',
              windRisk: '',
              userDataAvailable: false,
              lineGeoJSON: null,
              pointsGeoJSON: null,
              polygonsGeoJSON: null,
              surgeGeoJSON: null,
              windGeoJSON: null,
              windGrib2JSON: null,
            };
            observer.next(stormData);
            observer.complete();
            return;
          }
          const stormData: StormData = {
            lattitude: Number.parseFloat(result.storm.latitude),
            longitude: Number.parseFloat(result.storm.longitude),
            address: result.storm.address,
            clientId: Number.parseInt(result.storm.client_id),
            surgeRisk: result.storm.surgerisk,
            maxFlood: Number.parseFloat(result.storm.maxflood),
            forecastAdvisory: 0,
            advisoryDate: result.storm.advisory_date,
            floodAdvisoryDate: result.storm.advisory_flood_date,
            windAdvisoryDate: result.storm.advisory_wind_date,
            floodNextAdvisoryDate: result.storm.next_advisory_flood_date,
            windNextAdvisoryDate: result.storm.next_advisory_wind_date,
            nextAdvisoryDate: result.storm.next_advisory_date,
            landfallDate: moment(result.storm.landfall_datetime).toDate(),
            landfallLocation: result.storm.landfall_location,
            stormDistance: Number.parseFloat(result.storm.storm_distance),
            stormName: result.storm.storm_name,
            windRisk: result.storm.windrisk,
            userDataAvailable: result.storm.has_data,
            lineGeoJSON: JSON.parse(result.storm.line_data),
            pointsGeoJSON: JSON.parse(result.storm.points_data),
            polygonsGeoJSON: JSON.parse(result.storm.polygon_data),
            surgeGeoJSON: result.surge,
            windGeoJSON: result.wind.windGeoJSON,
            windGrib2JSON: result.wind.windGrib2JSON,
          };
          console.log(result.wind.windGeoJSON);
          if (stormData.windGeoJSON === null) {
            stormData.userDataAvailable = false;
          }
          stormData.lineGeoJSON.features = stormData.lineGeoJSON.features.map(
            (feature, index) => {
              const id = `line-${index + 1}`;
              const style = {
                clickable: false,
                draggable: false,
                editable: false,
                fillColor: feature.properties.fill,
                fillOpacity: feature.properties['fill-opacity'],
                strokeColor: feature.properties.stroke,
                strokeOpacity: feature.properties['stroke-opacity'],
                strokeWeight: feature.properties['stroke-width'],
                title: feature.properties.title,
                visible: false,
                zIndex: 30,
              };
              return {
                ...feature,
                properties: {
                  ...feature.properties,
                  id,
                  style,
                },
              };
            }
          );

          stormData.pointsGeoJSON.features = stormData.pointsGeoJSON.features.map(
            (feature, index) => {
              const id = `points-${index + 1}`;

              let markerIcon;
              if (index === 0) {
                const maxWind = feature.properties.MAXWIND;
                markerIcon = StormMarkerIcons[maxWind > 73 ? 'CH' : 'CTS'];
              } else {
                markerIcon = StormMarkerIcons[feature.properties.DVLBL];
              }

              const markerAnchor =
                index === 0
                  ? new google.maps.Point(25, 25)
                  : new google.maps.Point(10, 10);

              const markerSize =
                index === 0
                  ? new google.maps.Size(50, 50)
                  : new google.maps.Size(20, 20);

              const marker: google.maps.Icon = {
                url: markerIcon,
                anchor: markerAnchor,
                scaledSize: markerSize,
                size: markerSize,
              };
              const style = {
                clickable: false,
                draggable: false,
                editable: false,
                fillColor: feature.properties.fill,
                fillOpacity: feature.properties['fill-opacity'],
                strokeColor: feature.properties.stroke,
                strokeOpacity: feature.properties['stroke-opacity'],
                strokeWeight: feature.properties['stroke-width'],
                title: feature.properties.DVLBL,
                visible: false,
                icon: marker,
                zIndex: 40,
              };

              return {
                ...feature,
                properties: {
                  ...feature.properties,
                  id,
                  style,
                },
              };
            }
          );

          stormData.polygonsGeoJSON.features = stormData.polygonsGeoJSON.features.map(
            (feature, index) => {
              return {
                ...feature,
                properties: {
                  id: `polygons- ${index + 1}`,
                  ...feature.properties,
                  style: {
                    clickable: feature.properties.clickable,
                    cursor: feature.properties.cursor,
                    draggable: feature.properties.draggable,
                    editable: feature.properties.editable,
                    fillColor: feature.properties.fill,
                    fillOpacity: feature.properties.fillOpacity,
                    strokeColor: feature.properties.stroke,
                    strokeOpacity: feature.properties.strokeOpacity,
                    strokeWeight: 2,
                    title: feature.properties.title,
                    zIndex: 20,
                    visible: false,
                  },
                },
              };
            }
          );

          try {
            stormData.forecastAdvisory = Number.parseInt(
              stormData.pointsGeoJSON.features[0].properties.ADVISNUM
            );
          } catch (error) {
            console.log(error);
          }

          observer.next(stormData);
          observer.complete();
        });

      // .pipe(
      //   take(1),
      //   map((result) => {
      //     const stormData: StormData = {
      //       lattitude: Number.parseFloat(result.storm.latitude),
      //       longitude: Number.parseFloat(result.storm.latitude),
      //       address: result.storm.address,
      //       clientId: Number.parseInt(result.storm.client_id),
      //       surgeRisk: result.storm.surgerisk,
      //       maxFlood: Number.parseFloat(result.storm.maxflood),
      //       advisoryDate: result.storm.advisory_date,
      //       nextAdvisoryDate: result.storm.next_advisory_date,
      //       landfallDate: moment(result.storm.landfall_datetime).toDate(),
      //       landfallLocation: result.storm.landfall_location,
      //       stormDistance: Number.parseFloat(result.storm.storm_distance),
      //       stormName: result.storm.storm_name,
      //       windRisk: result.storm.windrisk,
      //       lineGeoJSON: JSON.parse(result.storm.line_data),
      //       pointsGeoJSON: JSON.parse(result.storm.points_data),
      //       polygonsGeoJSON: JSON.parse(result.storm.polygon_data),
      //       surgeGeoJSON: result.surge,
      //       windGeoJSON: result.wind.windGeoJSON,
      //       windGrib2JSON: result.wind.windGrib2JSON,
      //     };
      //     observer.next(stormData);
      //     observer.complete();
      //   })
      // );
    });
  }

  private getStormParameters(freeMode: boolean) {
    return this.httpClient.get<{
      latitude: string;
      longitude: string;
      address: string;
      client_id: string;
      surgerisk: string;
      maxflood: string;
      advisory_date: string;
      advisory_flood_date: string;
      advisory_wind_date: string;
      next_advisory_flood_date: string;
      next_advisory_wind_date: string;
      next_advisory_date: string;
      landfall_datetime: Date;
      landfall_location: string;
      storm_distance: string;
      storm_name: string;
      windrisk: string;
      line_data: string;
      points_data: string;
      polygon_data: string;
      has_data: boolean;
    }>(environment.API_URL + (freeMode ? '/storm-data/free' : '/storm-data'), {
      headers: { 'Content-type': 'application/json; charset=utf-8' },
      withCredentials: true,
    });
  }

  private getSurgeParameters() {
    return this.httpClient
      .get<{ url: string }>(environment.API_URL + '/surge-data', {
        headers: { 'Content-type': 'application/json; charset=utf-8' },
      })
      .pipe(
        take(1),
        switchMap(
          (response) =>
            this.httpClient.get(response.url, {
              observe: 'response',
              responseType: 'blob',
            })
          // this.httpClient.get(
          //   'https://zip-bucket-sumedh.s3.amazonaws.com/surge-2021-al06-20-202108141500.zip',
          //   {
          //     observe: 'response',
          //     responseType: 'blob',
          //   }
          // )
          // this.httpClient.get(
          //   'https://qrisq-angular-webspa.s3.us-east-2.amazonaws.com/surge-2020-al28-17-202010282100.zip',
          //   {
          //     observe: 'response',
          //     responseType: 'blob',
          //   }
          // )
          // this.httpClient.get(
          //   'https://api.qrisq.com/api/zip/surge-2020-al28-17-202010282100.zip',
          //   {
          //     observe: 'response',
          //     responseType: 'blob',
          //   }
          // )
        ),
        take(1),
        switchMap(
          (response) =>
            new Observable<Object>((observer) => {
              const url = URL.createObjectURL(response.body);
              loadshp(
                {
                  url,
                  encoding: 'ISO-8859-1',
                },
                (data: any) => {
                  let features = data.features.map((feature, index) => {
                    const maxft = feature.properties.maxft;
                    const id = 'surge-' + (index + 1).toString();
                    const color = getESRISurgeLevelColor(
                      Number.parseFloat(maxft)
                    );
                    const style = {
                      clickable: false,
                      draggable: false,
                      editable: false,
                      fillColor: color,
                      fillOpacity: 0.7,
                      strokeColor: color,
                      strokeWeight: 0.3,
                      strokeOpacity: 0.75,
                      visible: false,
                      color,
                    };

                    return {
                      ...feature,
                      properties: {
                        ...feature.properties,
                        id,
                        style,
                      },
                    };
                  });

                  // const features = data.features;
                  // const roundedFeatures = features.map((feature) => {
                  //   const result = feature.geometry.coordinates[0].map(
                  //     (coordinate) => [
                  //       Number(coordinate[0].toFixed(2)),
                  //       Number(coordinate[1].toFixed(2)),
                  //     ]
                  //   );
                  //   return {
                  //     ...feature,
                  //     geometry: { ...feature.geometry, coordinates: [result] },
                  //   };
                  // });
                  // console.log(roundedFeatures);
                  // const smoothFeatures = features.map((feature) => {
                  //   const result = smooth(
                  //     smooth(feature.geometry.coordinates[0])
                  //   );
                  //   return {
                  //     ...feature,
                  //     geometry: { ...feature.geometry, coordinates: [result] },
                  //   };
                  // });
                  const geoJson = { ...data, features };
                  observer.next(geoJson);
                  observer.complete();
                }
              );
            })
        )
      );
  }

  private getWindParameters() {
    return this.httpClient
      .get<{ json_data: string; js_data: string }>(
        // 'https://zip-bucket-sumedh.s3.amazonaws.com/surge-2021-al06-20-202108141500.zip',
        environment.API_URL + '/wind-data',
        {
          headers: {
            'Content-type': 'application/json; charset=utf-8',
          },
        }
      )
      .pipe(
        take(1),
        switchMap(
          (response) =>
            new Observable<{ windGeoJSON: Object; windGrib2JSON: Object }>(
              (observer) => {
                let windGeoJSON: Object;
                let windGrib2JSON: Object;
                try {
                  // process grib2 binary data
                  const data = JSON.parse(response.js_data);
                  if (data != '') {
                    let instances, vtime;
                    instances = Object.keys(data);
                    instances.sort();
                    let range = instances.length - 1;
                    vtime = instances[0];
                    if (!vtime) {
                      instances = Object.keys(data);
                      instances.sort();
                      vtime = instances[0];
                    }
                    const binData = atob(data[vtime]);
                    const charData = binData.split('').map(function (x) {
                      return x.charCodeAt(0);
                    });
                    var zlibData = new Uint8Array(charData);
                    const result = JSON.parse(
                      pako.inflate(zlibData, { to: 'string' })
                    );
                    result[0].data = Array(result[1].data.length).fill(280);
                    windGrib2JSON = result;
                  }
                  windGeoJSON = JSON.parse(response.json_data);
                  console.log(JSON.parse(response.json_data));
                  observer.next({ windGeoJSON, windGrib2JSON });
                  observer.complete();
                } catch (error) {
                  console.log(error);
                  observer.next({ windGeoJSON: null, windGrib2JSON: null });
                  observer.complete();
                }
              }
            )
        ),
        catchError((err) => {
          console.log('caught rethrown error, providing fallback value');
          return of({ windGeoJSON: null, windGrib2JSON: null });
        })
      );
  }
}
