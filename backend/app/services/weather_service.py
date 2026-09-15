import datetime
import httpx
from typing import Dict, Any, Optional
from app.config import settings
from app.data.seed_data import KERALA_DISTRICTS

# Fallback climatic profiles for Kerala districts in current season (September post-monsoon)
DISTRICT_WEATHER_DEFAULTS = {
    "Idukki": {
        "avg_temp": 23.5, "min_temp": 18.0, "max_temp": 26.5,
        "rainfall_7d": 42.0, "rain_prob": 65, "humidity": 78.0,
        "condition": "Light afternoon showers with clear mornings"
    },
    "Wayanad": {
        "avg_temp": 24.0, "min_temp": 19.0, "max_temp": 27.0,
        "rainfall_7d": 48.0, "rain_prob": 70, "humidity": 80.0,
        "condition": "Scattered monsoon showers with mist"
    },
    "Palakkad": {
        "avg_temp": 30.5, "min_temp": 24.0, "max_temp": 34.5,
        "rainfall_7d": 18.0, "rain_prob": 35, "humidity": 65.0,
        "condition": "Warm and sunny with occasional drizzle"
    },
    "Thrissur": {
        "avg_temp": 28.0, "min_temp": 23.5, "max_temp": 31.0,
        "rainfall_7d": 35.0, "rain_prob": 55, "humidity": 75.0,
        "condition": "Humid with passing coastal showers"
    },
    "Ernakulam": {
        "avg_temp": 28.5, "min_temp": 24.0, "max_temp": 31.5,
        "rainfall_7d": 38.0, "rain_prob": 60, "humidity": 78.0,
        "condition": "Coastal breeze with light rain"
    },
    "Alappuzha": {
        "avg_temp": 28.0, "min_temp": 24.0, "max_temp": 31.0,
        "rainfall_7d": 32.0, "rain_prob": 50, "humidity": 82.0,
        "condition": "Intermittent light rain over backwaters"
    },
    "Kottayam": {
        "avg_temp": 27.5, "min_temp": 23.0, "max_temp": 31.0,
        "rainfall_7d": 36.0, "rain_prob": 55, "humidity": 76.0,
        "condition": "Partly cloudy with pleasant daytime temperatures"
    }
}


WMO_WEATHER_CODES = {
    0: "Clear sky",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Foggy conditions",
    48: "Depositing rime fog",
    51: "Light drizzle",
    53: "Moderate drizzle",
    55: "Dense drizzle",
    61: "Slight rain",
    63: "Moderate rain",
    65: "Heavy rainfall",
    80: "Slight rain showers",
    81: "Moderate rain showers",
    82: "Violent rain showers",
    95: "Thunderstorm with rain"
}


async def get_weather_forecast(
    district: str,
    lat: Optional[float] = None,
    lon: Optional[float] = None
) -> Dict[str, Any]:
    """
    Fetches 7-day weather forecast:
    1. From OpenWeatherMap if OPENWEATHER_API_KEY is provided.
    2. Automatically from Open-Meteo (Free Live Global Weather API, zero-key required).
    3. Graceful fallback to Kerala agro-meteorological profile if offline.
    """
    district_clean = district.strip().title()
    district_meta = KERALA_DISTRICTS.get(district_clean, KERALA_DISTRICTS["Idukki"])

    latitude = lat if lat is not None else district_meta.get("lat", 9.8494)
    longitude = lon if lon is not None else district_meta.get("lon", 76.9814)

    # 1. OpenWeatherMap (if user provided API key)
    if settings.OPENWEATHER_API_KEY:
        try:
            url = "https://api.openweathermap.org/data/2.5/forecast"
            params = {
                "lat": latitude,
                "lon": longitude,
                "appid": settings.OPENWEATHER_API_KEY,
                "units": "metric"
            }
            async with httpx.AsyncClient(timeout=6.0) as client:
                resp = await client.get(url, params=params)
                if resp.status_code == 200:
                    data = resp.json()
                    entries = data.get("list", [])
                    if entries:
                        temps = [e["main"]["temp"] for e in entries[:24]]
                        rain_total = sum(e.get("rain", {}).get("3h", 0.0) for e in entries[:24])
                        humidities = [e["main"]["humidity"] for e in entries[:24]]
                        main_cond = entries[0]["weather"][0]["description"]

                        return {
                            "avg_temp_c": round(float(sum(temps) / len(temps)), 1),
                            "min_temp_c": round(float(min(temps)), 1),
                            "max_temp_c": round(float(max(temps)), 1),
                            "total_rainfall_next_7d_mm": round(float(rain_total * 2), 1),
                            "rain_probability_pct": int(data.get("list", [{}])[0].get("pop", 0.5) * 100),
                            "humidity_avg_pct": round(float(sum(humidities) / len(humidities)), 1),
                            "weather_condition": main_cond.title(),
                            "is_live_data": True,
                            "provider": "OpenWeatherMap API"
                        }
        except Exception:
            pass

    # 2. Open-Meteo Live API (Free, Real-Time Live Weather for all Kerala coordinates, Zero-Key)
    try:
        om_url = (
            f"https://api.open-meteo.com/v1/forecast"
            f"?latitude={latitude}&longitude={longitude}"
            f"&current=temperature_2m,relative_humidity_2m,weather_code"
            f"&daily=temperature_2m_max,temperature_2m_min,precipitation_sum,precipitation_probability_max"
            f"&timezone=Asia%2FKolkata"
        )
        async with httpx.AsyncClient(timeout=8.0) as client:
            resp = await client.get(om_url)
            if resp.status_code == 200:
                om_data = resp.json()
                current = om_data.get("current", {})
                daily = om_data.get("daily", {})

                max_temps = daily.get("temperature_2m_max", [28.0])
                min_temps = daily.get("temperature_2m_min", [22.0])
                rain_sums = daily.get("precipitation_sum", [5.0])
                rain_probs = daily.get("precipitation_probability_max", [60])

                avg_t = round(float((sum(max_temps) + sum(min_temps)) / (2 * len(max_temps))), 1)
                total_rain_7d = round(float(sum(rain_sums)), 1)
                max_prob = int(max(rain_probs)) if rain_probs else 60
                w_code = current.get("weather_code", 3)
                cond_desc = WMO_WEATHER_CODES.get(w_code, "Partly cloudy with scattered rain")

                return {
                    "avg_temp_c": avg_t,
                    "min_temp_c": round(float(min(min_temps)), 1),
                    "max_temp_c": round(float(max(max_temps)), 1),
                    "total_rainfall_next_7d_mm": total_rain_7d,
                    "rain_probability_pct": max_prob,
                    "humidity_avg_pct": float(current.get("relative_humidity_2m", 78.0)),
                    "weather_condition": cond_desc,
                    "is_live_data": True,
                    "provider": "Open-Meteo Live Global Meteorological API"
                }
    except Exception:
        pass

    # Reliable agronomic baseline for hackathons & offline demonstrations
    base = DISTRICT_WEATHER_DEFAULTS.get(
        district_clean,
        {
            "avg_temp": 26.5, "min_temp": 21.0, "max_temp": 30.5,
            "rainfall_7d": 30.0, "rain_prob": 50, "humidity": 75.0,
            "condition": "Scattered clouds with mild rain"
        }
    )

    return {
        "avg_temp_c": base["avg_temp"],
        "min_temp_c": base["min_temp"],
        "max_temp_c": base["max_temp"],
        "total_rainfall_next_7d_mm": base["rainfall_7d"],
        "rain_probability_pct": base["rain_prob"],
        "humidity_avg_pct": base["humidity"],
        "weather_condition": base["condition"],
        "is_live_data": False
    }
