import { HourlyWeather } from '../types.js';

interface OpenMeteoResponse {
  hourly: {
    time: string[];
    temperature_2m: number[];
    apparent_temperature: number[];
    relative_humidity_2m: number[];
    precipitation_probability: number[];
    weather_code: number[];
  };
}

export async function fetchHourlyWeather(
  latitude: number,
  longitude: number,
  hours: number = 24
): Promise<HourlyWeather[]> {
  const url = new URL('https://api.open-meteo.com/v1/forecast');
  url.searchParams.set('latitude', latitude.toString());
  url.searchParams.set('longitude', longitude.toString());
  url.searchParams.set(
    'hourly',
    'temperature_2m,apparent_temperature,relative_humidity_2m,precipitation_probability,weather_code'
  );
  url.searchParams.set('timezone', 'auto');
  url.searchParams.set('forecast_hours', hours.toString());

  const response = await fetch(url.toString(), {
    headers: { Accept: 'application/json' },
  });

  if (!response.ok) {
    throw new Error(`Open-Meteo API error: ${response.status} ${response.statusText}`);
  }

  const data = (await response.json()) as OpenMeteoResponse;

  const { time, temperature_2m, apparent_temperature, relative_humidity_2m, precipitation_probability, weather_code } = data.hourly;

  return time.map((t, i) => ({
    time: t,
    temperature: temperature_2m[i]!,
    apparentTemperature: apparent_temperature[i]!,
    humidity: relative_humidity_2m[i]!,
    precipitationProbability: precipitation_probability[i]!,
    weatherCode: weather_code[i]!,
  }));
}
