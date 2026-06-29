from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import Any

import requests

API_BASE = os.environ.get("API_BASE", "http://localhost:3001/api")

# WMO weather code → emoji + label
WEATHER_CODES: dict[int, tuple[str, str]] = {
    0: ("☀️", "Clear"),
    1: ("🌤", "Mainly Clear"),
    2: ("⛅", "Partly Cloudy"),
    3: ("☁️", "Overcast"),
    45: ("🌫", "Foggy"),
    48: ("🌫", "Rime Fog"),
    51: ("🌦", "Light Drizzle"),
    53: ("🌦", "Moderate Drizzle"),
    55: ("🌧", "Dense Drizzle"),
    56: ("🌧", "Freezing Drizzle"),
    57: ("🌧", "Dense Freezing Drizzle"),
    61: ("🌦", "Slight Rain"),
    63: ("🌧", "Moderate Rain"),
    65: ("🌧", "Heavy Rain"),
    66: ("🌧", "Freezing Rain"),
    67: ("🌧", "Heavy Freezing Rain"),
    71: ("🌨", "Slight Snow"),
    73: ("🌨", "Moderate Snow"),
    75: ("❄️", "Heavy Snow"),
    77: ("❄️", "Snow Grains"),
    80: ("🌦", "Rain Showers"),
    81: ("🌧", "Moderate Rain Showers"),
    82: ("🌧", "Violent Rain Showers"),
    85: ("🌨", "Snow Showers"),
    86: ("❄️", "Heavy Snow Showers"),
    95: ("⛈", "Thunderstorm"),
    96: ("⛈", "Thunderstorm & Hail"),
    99: ("⛈", "Thunderstorm & Heavy Hail"),
}


def weather_icon(code: int) -> str:
    return WEATHER_CODES.get(code, ("❓", "Unknown"))[0]


def weather_label(code: int) -> str:
    return WEATHER_CODES.get(code, ("❓", "Unknown"))[1]


@dataclass
class StateSummary:
    name: str
    abbreviation: str
    capital: str


@dataclass
class HourlyWeather:
    time: str
    temperature: float
    apparent_temperature: float
    humidity: int
    precipitation_probability: int
    weather_code: int

    @property
    def icon(self) -> str:
        return weather_icon(self.weather_code)

    @property
    def label(self) -> str:
        return weather_label(self.weather_code)


@dataclass
class WeatherResponse:
    state: dict[str, Any]
    current: HourlyWeather
    hourly: list[HourlyWeather]
    summary: str | None
    updated_at: str


def _to_snake(d: dict[str, Any]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for k, v in d.items():
        snake = "".join("_" + c.lower() if c.isupper() else c for c in k).lstrip("_")
        result[snake] = v
    return result


def _get_json(path: str) -> Any:
    url = f"{API_BASE}{path}"
    resp = requests.get(url, timeout=10)
    resp.raise_for_status()
    return resp.json()


def fetch_states() -> list[StateSummary]:
    data = _get_json("/states")
    return [StateSummary(**s) for s in data]


def fetch_weather(state: str) -> WeatherResponse:
    data = _get_json(f"/weather?state={state}")
    hourly = [HourlyWeather(**_to_snake(h)) for h in data["hourly"]]
    return WeatherResponse(
        state=data["state"],
        current=HourlyWeather(**_to_snake(data["current"])),
        hourly=hourly,
        summary=data.get("summary"),
        updated_at=data["updatedAt"],
    )
