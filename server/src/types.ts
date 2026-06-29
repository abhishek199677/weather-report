export interface StateInfo {
  name: string;
  abbreviation: string;
  capital: string;
  latitude: number;
  longitude: number;
}

export interface HourlyWeather {
  time: string;
  temperature: number;
  apparentTemperature: number;
  humidity: number;
  precipitationProbability: number;
  weatherCode: number;
}

export interface WeatherResponse {
  state: StateInfo;
  current: HourlyWeather;
  hourly: HourlyWeather[];
  summary: string | null;
  updatedAt: string;
}
