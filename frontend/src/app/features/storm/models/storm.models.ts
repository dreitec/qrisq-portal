export interface StormData {
  clientId: number;
  lattitude: number;
  longitude: number;
  stormName: string;
  address: string;
  windRisk: string;
  surgeRisk: string;
  forecastAdvisory: number;
  advisoryDate: string;
  floodAdvisoryDate: string;
  windAdvisoryDate: string;
  floodNextAdvisoryDate: string;
  windNextAdvisoryDate: string;
  nextAdvisoryDate: string;
  maxFlood: number;
  landfallLocation: string;
  landfallDate: Date;
  stormDistance: number;
  lineGeoJSON: any;
  pointsGeoJSON: any;
  polygonsGeoJSON: any;
  surgeGeoJSON: any;
  windGeoJSON: any;
  windGrib2JSON: any;
  userDataAvailable: boolean;
}

export interface StormParameters {
  client_id: number;
  storm_name: string;
  latitude: string;
  longitude: string;
  address: string;
  advisory_date: string;
  next_advisory_date: string;
  line_data: string;
  points_data: string;
  polygon_data: string;
  windrisk: string;
  surgerisk: string;
  maxflood: string;
  landfall_location: string;
  landfall_datetime: string;
  storm_distance: string;
  maxflood_datetime: string;
  maxwind_datetime: string;
  had_data: boolean;
}

export enum WindRiskLevelId {
  Category1 = '1',
  Category2 = '2',
  Category3 = '3',
  Category4 = '4',
  Category5 = '5',
  Minimal = 'N',
  TropicalStorm = 'TS',
}

export interface WindRiskLevel {
  id: WindRiskLevelId;
  shortDesc: string;
  speedDesc: string;
  colorHex: string;
  iconUrl: string;
}

export enum SurgeRiskLevelId {
  NoRisk = 'N',
  LowRisk = 'L',
  ModerateRisk = 'M',
  HighRisk = 'H',
}

export interface SurgeRiskLevel {
  id: SurgeRiskLevelId;
  riskDesc: string;
  levelDesc: string;
  colorHex: string;
  iconUrl: string;
}
