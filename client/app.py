from __future__ import annotations

from datetime import datetime

import pandas as pd
import streamlit as st

from api_client import WeatherResponse, fetch_states, fetch_weather

# ── Page Config ──

st.set_page_config(
    page_title="Weather Report — India",
    page_icon="🇮🇳",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Session State ──

for key, default in [("weather", None), ("error", None)]:
    if key not in st.session_state:
        st.session_state[key] = default

# ── Cached Helpers ──


@st.cache_data(ttl=3600)
def load_states():
    return fetch_states()


# ── Render Functions ──


def render_summary_box(w: WeatherResponse) -> None:
    if not w.summary:
        return
    st.info(f"🤖 {w.summary}")


def render_current(w: WeatherResponse) -> None:
    cur = w.current
    st.markdown(
        f"## {w.state['capital']}, {w.state['name']}   \n"
        f"{cur.icon} **{cur.label}** — feels like {cur.apparent_temperature:.0f}°C"
    )

    cols = st.columns(4)
    metrics = [
        ("🌡 Temperature", f"{cur.temperature:.0f}°C"),
        ("💧 Humidity", f"{cur.humidity}%"),
        ("🌧 Precip.", f"{cur.precipitation_probability}%"),
        ("🕒 Updated", datetime.fromisoformat(w.updated_at).strftime("%H:%M")),
    ]
    for col, (label, value) in zip(cols, metrics):
        with col:
            st.metric(label, value)


def render_hourly_chart(hourly: list) -> None:
    df = pd.DataFrame(
        [
            {
                "Time": datetime.fromisoformat(h.time).strftime("%H:%M"),
                "Temperature (°C)": round(h.temperature, 1),
                "Feels Like (°C)": round(h.apparent_temperature, 1),
            }
            for h in hourly
        ]
    ).set_index("Time")

    st.subheader("24-Hour Temperature Trend")
    st.line_chart(df, height=280, use_container_width=True)


def render_hourly_table(hourly: list) -> None:
    rows = []
    for h in hourly:
        dt = datetime.fromisoformat(h.time)
        rows.append(
            {
                "Time": dt.strftime("%a %H:%M"),
                "": h.icon,
                "Condition": h.label,
                "Temp": f"{h.temperature:.0f}°C",
                "Feels Like": f"{h.apparent_temperature:.0f}°C",
                "Humidity": f"{h.humidity}%",
                "Precip.": f"{h.precipitation_probability}%",
            }
        )

    st.subheader("Hourly Details")
    st.dataframe(
        pd.DataFrame(rows),
        column_config={
            "": st.column_config.TextColumn("", width="small"),
            "Condition": st.column_config.TextColumn("Condition", width="medium"),
            "Temp": st.column_config.TextColumn("Temp", width="small"),
            "Feels Like": st.column_config.TextColumn("Feels Like", width="small"),
            "Humidity": st.column_config.TextColumn("Humidity", width="small"),
            "Precip.": st.column_config.TextColumn("Precip.", width="small"),
        },
        hide_index=True,
        use_container_width=True,
        height=min(35 * len(rows) + 38, 600),
    )


def render_weather(w: WeatherResponse) -> None:
    render_summary_box(w)
    render_current(w)
    st.divider()
    render_hourly_chart(w.hourly)
    with st.expander("📋 View full hourly table", expanded=False):
        render_hourly_table(w.hourly)


# ── Load States ──

try:
    states = load_states()
except Exception as exc:
    st.error(f"Failed to load states: {exc}")
    st.stop()

state_options = {f"{s.name} ({s.abbreviation}) — {s.capital}": s.abbreviation for s in states}
sorted_labels = sorted(state_options.keys())

# ── Sidebar ──

with st.sidebar:
    st.title("🇮🇳 States & UTs")
    selected_label = st.selectbox(
        "Choose a state",
        options=sorted_labels,
        index=None,
        placeholder="Search or select a state…",
        label_visibility="collapsed",
    )

    st.divider()

    col1, col2 = st.columns(2)
    with col1:
        refresh = st.button("🔄 Refresh", use_container_width=True, type="secondary")
    with col2:
        clear = st.button("Clear", use_container_width=True, type="secondary")

    if clear:
        st.session_state.weather = None
        st.session_state.error = None

    st.divider()
    st.caption("Weather by [Open-Meteo](https://open-meteo.com) · AI by OpenAI")

# ── Main Area ──

st.title("🇮🇳 Weather Report — India")
st.markdown("Hourly weather for **Indian state and union territory capitals**")

# Nothing selected — show placeholder or existing data
if not selected_label:
    if st.session_state.weather is not None and not clear:
        render_weather(st.session_state.weather)
    else:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.info("👈 Select a state or UT from the sidebar to view its capital's weather")
    st.stop()

selected_abbr = state_options[selected_label]

# ── Fetch Weather (if needed) ──

needs_fetch = (
    st.session_state.weather is None
    or st.session_state.weather.state["abbreviation"] != selected_abbr
    or refresh
)

if needs_fetch:
    with st.spinner("Fetching weather data & generating AI summary…"):
        try:
            st.session_state.weather = fetch_weather(selected_abbr)
            st.session_state.error = None
        except Exception as exc:
            st.session_state.error = str(exc)
            st.session_state.weather = None

if st.session_state.error:
    st.error(f"Failed to load weather data: {st.session_state.error}")

    def _retry():
        st.session_state.weather = None
        st.session_state.error = None

    st.button("🔄 Retry", on_click=_retry, type="primary")
    st.stop()

if st.session_state.weather is not None:
    render_weather(st.session_state.weather)
