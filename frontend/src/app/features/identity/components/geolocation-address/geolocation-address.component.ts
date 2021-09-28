// angular
import {
  ApplicationRef,
  Component,
  ElementRef,
  Inject,
  Input,
  OnChanges,
  PLATFORM_ID,
  ViewChild,
} from '@angular/core';
import { isPlatformBrowser } from '@angular/common';

// google maps
import { MapsAPILoader } from '@agm/core';

@Component({
  selector: 'qr-geolocation-address',
  templateUrl: './geolocation-address.component.html',
  styleUrls: ['./geolocation-address.component.scss'],
})
export class QrGeolocationAddressComponent implements OnChanges {
  @ViewChild('streetviewMap', { static: true }) streetviewMap: ElementRef;
  @ViewChild('streetviewPano', { static: true }) streetviewPano: ElementRef;
  @Input() latitude: number;
  @Input() longitude: number;
  @Input() zoom = 11;
  @Input() heading = 34;
  @Input() pitch = 10;
  @Input() scrollwheel = false;

  constructor(
    @Inject(PLATFORM_ID) private platformId: Object,
    private mapsAPILoader: MapsAPILoader,
    private appRef: ApplicationRef
  ) {}

  ngOnChanges() {
    this.renderStreetView();
  }

  renderStreetView() {
    if (isPlatformBrowser(this.platformId)) {
      this.mapsAPILoader.load().then(() => {
        // const center = { lat: +this.latitude, lng: +this.longitude };
        const center = { lat: +this.latitude, lng: +this.longitude };
        const map = new window['google'].maps.Map(
          this.streetviewMap.nativeElement
        );
        const panorama = new window['google'].maps.StreetViewPanorama(
          this.streetviewPano.nativeElement,
          {
            position: center,
            pov: { heading: this.heading, pitch: this.pitch },
            scrollwheel: this.scrollwheel,
          }
        );
        map.setStreetView(panorama);
        this.appRef.tick();
      });
    }
  }
}
