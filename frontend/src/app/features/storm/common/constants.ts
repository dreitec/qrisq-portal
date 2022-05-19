import {
  WindRiskLevelId,
  WindRiskLevel,
  SurgeRiskLevelId,
  SurgeRiskLevel,
} from '../models/storm.models';

export const WindRiskLevels: Record<WindRiskLevelId, Partial<WindRiskLevel>> = {
  N: {
    id: WindRiskLevelId.Minimal,
    shortDesc: 'Minimal',
    speedDesc: '(<39 MPH)',
    colorHex: '#000',
    iconUrl: 'assets/icons/minimal-wind.png',
  },
  TS: {
    id: WindRiskLevelId.TropicalStorm,
    shortDesc: 'Tropical Storm',
    speedDesc: '(39-73 MPH)',
    colorHex: '#0404f7',
    iconUrl: 'assets/icons/tropicalstorm-wind.png',
  },
  '1': {
    id: WindRiskLevelId.Category1,
    shortDesc: 'Cat 1',
    speedDesc: '(74-95 MPH)',
    colorHex: '#04f7f7',
    iconUrl: 'assets/icons/category1-wind.png',
  },
  '2': {
    id: WindRiskLevelId.Category2,
    shortDesc: 'Cat 2',
    speedDesc: '96-(110 MPH)',
    colorHex: '#04f704',
    iconUrl: 'assets/icons/category2-wind.png',
  },
  '3': {
    id: WindRiskLevelId.Category3,
    shortDesc: 'Cat 3',
    speedDesc: '111-(129 MPH)',
    colorHex: '#f7f704',
    iconUrl: 'assets/icons/category3-wind.png',
  },
  '4': {
    id: WindRiskLevelId.Category4,
    shortDesc: 'Cat 4',
    speedDesc: '130-(156 MPH)',
    colorHex: '#f7a804',
    iconUrl: 'assets/icons/category4-wind.png',
  },
  '5': {
    id: WindRiskLevelId.Category5,
    shortDesc: 'Cat 5',
    speedDesc: '(157 < MPH)',
    colorHex: '#f70404',
    iconUrl: 'assets/icons/category5-wind.png',
  },
};

export const SurgeRiskLevels: Record<
  SurgeRiskLevelId,
  Partial<SurgeRiskLevel>
> = {
  N: {
    id: SurgeRiskLevelId.NoRisk,
    riskDesc: 'No',
    levelDesc: '-',
    colorHex: '#000',
    iconUrl: 'assets/icons/no-risk.png',
  },
  L: {
    id: SurgeRiskLevelId.LowRisk,
    riskDesc: 'Low',
    levelDesc: 'Surge Nearby',
    colorHex: '#f7f704',
    iconUrl: 'assets/icons/low-risk.png',
  },
  M: {
    id: SurgeRiskLevelId.ModerateRisk,
    riskDesc: 'Moderate',
    levelDesc: 'Up to 3ft.',
    colorHex: '#f7a804',
    iconUrl: 'assets/icons/moderate-risk.png',
  },
  H: {
    id: SurgeRiskLevelId.HighRisk,
    riskDesc: 'High',
    levelDesc: 'More than 3ft.',
    colorHex: '#f70404',
    iconUrl: 'assets/icons/high-risk.png',
  },
};

export const StormMarkerIcons = {
  L: '/assets/icons/storm-marker-icons/tropical-low.png',
  D: '/assets/icons/storm-marker-icons/tropical-depression.png',
  S: '/assets/icons/storm-marker-icons/tropical-storm.png',
  H: '/assets/icons/storm-marker-icons/tropical-hurricane.png',
  M: '/assets/icons/storm-marker-icons/mayor-depression.png',
  CH: '/assets/icons/storm-marker-icons/center-hurricane.png',
  CTS: '/assets/icons/storm-marker-icons/center-tropical-storm.png',
};
