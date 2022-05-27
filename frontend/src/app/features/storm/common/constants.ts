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
    speedDesc: '',
    colorHex: '#000',
    iconUrl: 'assets/icons/minimal-wind.png',
    iconUrlx2: 'assets/icons/minimal-wind@x2.png',
  },
  TS: {
    id: WindRiskLevelId.TropicalStorm,
    shortDesc: 'Tropical Storm',
    speedDesc: '39-73 MPH',
    colorHex: '#0404f7',
    iconUrl: 'assets/icons/tropicalstorm-wind.png',
    iconUrlx2: 'assets/icons/tropicalstorm-wind@x2.png',
  },
  '1': {
    id: WindRiskLevelId.Category1,
    shortDesc: 'Category 1',
    speedDesc: '74-95 MPH',
    colorHex: '#04f7f7',
    iconUrl: 'assets/icons/category1-wind.png',
    iconUrlx2: 'assets/icons/category1-wind@x2.png',
  },
  '2': {
    id: WindRiskLevelId.Category2,
    shortDesc: 'Category 2',
    speedDesc: '96-110 MPH',
    colorHex: '#04f704',
    iconUrl: 'assets/icons/category2-wind.png',
    iconUrlx2: 'assets/icons/category2-wind@x2.png',
  },
  '3': {
    id: WindRiskLevelId.Category3,
    shortDesc: 'Category 3',
    speedDesc: '111-129 MPH',
    colorHex: '#f7f704',
    iconUrl: 'assets/icons/category3-wind.png',
    iconUrlx2: 'assets/icons/category3-wind@x2.png',
  },
  '4': {
    id: WindRiskLevelId.Category4,
    shortDesc: 'Category 4',
    speedDesc: '130-156 MPH',
    colorHex: '#f7a804',
    iconUrl: 'assets/icons/category4-wind.png',
    iconUrlx2: 'assets/icons/category4-wind@x2.png',
  },
  '5': {
    id: WindRiskLevelId.Category5,
    shortDesc: 'Category 5',
    speedDesc: '157 < MPH',
    colorHex: '#f70404',
    iconUrl: 'assets/icons/category5-wind.png',
    iconUrlx2: 'assets/icons/category5-wind@x2.png',
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
    iconUrlx2: 'assets/icons/no-risk@x2.png',
  },
  L: {
    id: SurgeRiskLevelId.LowRisk,
    riskDesc: 'Low',
    levelDesc: 'Surge Nearby',
    colorHex: '#f7f704',
    iconUrl: 'assets/icons/low-risk.png',
    iconUrlx2: 'assets/icons/low-risk@x2.png',
  },
  M: {
    id: SurgeRiskLevelId.ModerateRisk,
    riskDesc: 'Moderate',
    levelDesc: 'Up to 3ft.',
    colorHex: '#f7a804',
    iconUrl: 'assets/icons/moderate-risk.png',
    iconUrlx2: 'assets/icons/moderate-risk@x2.png',
  },
  H: {
    id: SurgeRiskLevelId.HighRisk,
    riskDesc: 'High',
    levelDesc: 'More than 3ft.',
    colorHex: '#f70404',
    iconUrl: 'assets/icons/high-risk.png',
    iconUrlx2: 'assets/icons/high-risk@x2.png',
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

export const WindDirectionAndDegrees = [
  {
    direction: 'N',
    degreeFrom: 348.75,
    degreeTo: 11.25,
  },
  {
    direction: 'NNE',
    degreeFrom: 11.25,
    degreeTo: 33.75,
  },
  {
    direction: 'NE',
    degreeFrom: 33.75,
    degreeTo: 56.25,
  },
  {
    direction: 'ENE',
    degreeFrom: 56.25,
    degreeTo: 78.75,
  },
  {
    direction: 'E',
    degreeFrom: 78.75,
    degreeTo: 101.25,
  },
  {
    direction: 'ESE',
    degreeFrom: 101.25,
    degreeTo: 123.75,
  },
  {
    direction: 'SE',
    degreeFrom: 123.75,
    degreeTo: 146.25,
  },
  {
    direction: 'SSE',
    degreeFrom: 146.25,
    degreeTo: 168.75,
  },
  {
    direction: 'S',
    degreeFrom: 168.75,
    degreeTo: 191.25,
  },
  {
    direction: 'SSW',
    degreeFrom: 191.25,
    degreeTo: 213.75,
  },
  {
    direction: 'SW',
    degreeFrom: 213.75,
    degreeTo: 236.25,
  },
  {
    direction: 'WSW',
    degreeFrom: 236.25,
    degreeTo: 258.75,
  },
  {
    direction: 'W',
    degreeFrom: 258.75,
    degreeTo: 281.25,
  },
  {
    direction: 'WNW',
    degreeFrom: 281.25,
    degreeTo: 303.75,
  },
  {
    direction: 'NW',
    degreeFrom: 303.75,
    degreeTo: 326.25,
  },
  {
    direction: 'NNW',
    degreeFrom: 326.25,
    degreeTo: 348.75,
  },
];
