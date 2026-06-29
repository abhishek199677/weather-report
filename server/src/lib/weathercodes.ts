const weatherCodeMap: Record<number, { label: string; icon: string }> = {
  0:  { label: 'Clear', icon: '☀️' },
  1:  { label: 'Mainly Clear', icon: '🌤' },
  2:  { label: 'Partly Cloudy', icon: '⛅' },
  3:  { label: 'Overcast', icon: '☁️' },
  45: { label: 'Foggy', icon: '🌫' },
  48: { label: 'Depositing Rime Fog', icon: '🌫' },
  51: { label: 'Light Drizzle', icon: '🌦' },
  53: { label: 'Moderate Drizzle', icon: '🌦' },
  55: { label: 'Dense Drizzle', icon: '🌧' },
  56: { label: 'Light Freezing Drizzle', icon: '🌧' },
  57: { label: 'Dense Freezing Drizzle', icon: '🌧' },
  61: { label: 'Slight Rain', icon: '🌦' },
  63: { label: 'Moderate Rain', icon: '🌧' },
  65: { label: 'Heavy Rain', icon: '🌧' },
  66: { label: 'Light Freezing Rain', icon: '🌧' },
  67: { label: 'Heavy Freezing Rain', icon: '🌧' },
  71: { label: 'Slight Snow', icon: '🌨' },
  73: { label: 'Moderate Snow', icon: '🌨' },
  75: { label: 'Heavy Snow', icon: '❄️' },
  77: { label: 'Snow Grains', icon: '❄️' },
  80: { label: 'Slight Rain Showers', icon: '🌦' },
  81: { label: 'Moderate Rain Showers', icon: '🌧' },
  82: { label: 'Violent Rain Showers', icon: '🌧' },
  85: { label: 'Slight Snow Showers', icon: '🌨' },
  86: { label: 'Heavy Snow Showers', icon: '❄️' },
  95: { label: 'Thunderstorm', icon: '⛈' },
  96: { label: 'Thunderstorm with Slight Hail', icon: '⛈' },
  99: { label: 'Thunderstorm with Heavy Hail', icon: '⛈' },
};

export function getWeatherDescription(code: number): string {
  return weatherCodeMap[code]?.label ?? 'Unknown';
}

export function getWeatherIcon(code: number): string {
  return weatherCodeMap[code]?.icon ?? '❓';
}
