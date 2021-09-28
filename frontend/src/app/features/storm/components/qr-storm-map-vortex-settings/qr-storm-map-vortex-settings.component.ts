import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'qr-storm-map-vortex-settings',
  templateUrl: './qr-storm-map-vortex-settings.component.html',
  styleUrls: ['./qr-storm-map-vortex-settings.component.scss'],
})
export class QrStormMapVortexSettingsComponent implements OnInit {
  constructor() {}

  ngOnInit() {}

  // onVelocityScaleAfterChange(velocityScale: number) {
  //   this.vortexConfig = {
  //     ...this.vortexConfig,
  //     velocityScale: velocityScale,
  //   };
  //   this.updateVortexConfig();
  // }

  // onFrameRateAfterChange(frameRate: number) {
  //   this.vortexConfig = {
  //     ...this.vortexConfig,
  //     frameRate,
  //   };
  //   this.updateVortexConfig();
  // }

  // onParticleReductionAfterChange(particleReduction: number) {
  //   this.vortexConfig = {
  //     ...this.vortexConfig,
  //     particleReduction,
  //   };
  //   this.updateVortexConfig();
  // }

  // onParticleMultiplierAfterChange(particleMultiplier: number) {
  //   this.vortexConfig = {
  //     ...this.vortexConfig,
  //     particleMultiplier,
  //   };
  //   this.updateVortexConfig();
  // }

  // onParticleLineWidthAfterChange(particleLineWidth: number) {
  //   this.vortexConfig = {
  //     ...this.vortexConfig,
  //     particleLineWidth,
  //   };
  //   this.updateVortexConfig();
  // }

  // onMaxParticleAgeAfterChange(maxParticleAge: number) {
  //   this.vortexConfig = {
  //     ...this.vortexConfig,
  //     maxParticleAge,
  //   };
  //   this.updateVortexConfig();
  // }

  // onMaxWindIntensityAfterChange(maxWindIntensity: number) {
  //   this.vortexConfig = {
  //     ...this.vortexConfig,
  //     maxWindIntensity,
  //   };
  //   this.updateVortexConfig();
  // }

  // onIntensityScaleStepAfterChange(intensityScaleStep: number) {
  //   this.vortexConfig = {
  //     ...this.vortexConfig,
  //     intensityScaleStep,
  //   };
  //   this.updateVortexConfig();
  // }

  // onSettingsClick($event) {
  //   this.isSettingsVisible = true;
  // }

  // updateVortexConfig() {
  //   // const vortexConfig = {
  //   //   velocityScale: 0.08,
  //   //   intensityScaleStep: 2,
  //   //   maxWindIntensity: 10,
  //   //   maxParticleAge: 50,
  //   //   particleLineWidth: 0.15,
  //   //   particleMultiplier: 1 / 30,
  //   //   particleReduction: 0.8,
  //   //   frameRate: 20,
  //   // };

  //   this.windy.setVortexConfig(this.vortexConfig);
  //   this.windy.stop();
  //   let bounds = this.map.getBounds();
  //   let mapSizeX = this.map.getDiv().offsetWidth;
  //   let mapSizeY = this.map.getDiv().offsetHeight;
  //   this.windy.start(
  //     [
  //       [0, 0],
  //       [mapSizeX, mapSizeY],
  //     ],
  //     mapSizeX,
  //     mapSizeY,
  //     [
  //       [bounds.getSouthWest().lng(), bounds.getSouthWest().lat()],
  //       [bounds.getNorthEast().lng(), bounds.getNorthEast().lat()],
  //     ]
  //   );
  // }
}
