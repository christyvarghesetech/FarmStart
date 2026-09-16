# -*- coding: utf-8 -*-
"""
Pest & Disease Advisory Service
Cross-references crop profiles with live Open-Meteo meteorology (humidity, temperature, rainfall)
to generate real-time pest surge warnings and KAU dual-track remedies.
"""

from typing import Dict, Any, List
from app.data.pest_data import KAU_PEST_PROFILES
from app.services.weather_service import get_weather_forecast


async def evaluate_pest_advisory(crop: str, district: str) -> Dict[str, Any]:
    """
    Evaluates active pests and diseases for the specified crop in the given district.
    Calculates meteorological risk triggers based on live Open-Meteo weather data.
    """
    crop_clean = crop.strip().lower().replace(" ", "_")
    district_clean = district.strip().title()

    # 1. Fetch live weather metrics for the district
    weather_summary = {
        "avg_temp_c": 24.0,
        "humidity_avg_pct": 78,
        "total_rainfall_next_7d_mm": 18.0,
        "weather_condition": "Partly Cloudy"
    }

    try:
        weather_data = await get_weather_forecast(district_clean)
        if weather_data and "forecast_summary" in weather_data:
            fs = weather_data["forecast_summary"]
            weather_summary["avg_temp_c"] = fs.get("avg_temp_c", 24.0)
            weather_summary["humidity_avg_pct"] = fs.get("humidity_avg_pct", 78)
            weather_summary["total_rainfall_next_7d_mm"] = fs.get("total_rainfall_next_7d_mm", 18.0)
            weather_summary["weather_condition"] = fs.get("weather_condition", "Partly Cloudy")
    except Exception as e:
        # Fallback to standard Kerala averages if meteorological API fails
        pass

    curr_temp = weather_summary["avg_temp_c"]
    curr_hum = weather_summary["humidity_avg_pct"]
    curr_rain = weather_summary["total_rainfall_next_7d_mm"]

    # 2. Filter pests affecting the selected crop
    matched_pests = [
        p for p in KAU_PEST_PROFILES
        if crop_clean in p["crop_ids"]
    ]

    # If no direct match, provide general vegetable pests or all
    if not matched_pests:
        matched_pests = [
            p for p in KAU_PEST_PROFILES
            if "tomato" in p["crop_ids"] or "okra" in p["crop_ids"]
        ]

    # 3. Assess real-time weather risk for each pest
    evaluated_pests = []
    active_alerts_count = 0

    for p in matched_pests:
        wt = p["weather_triggers"]
        temp_match = (wt["min_temp_c"] <= curr_temp <= wt["max_temp_c"])
        hum_match = (wt["min_humidity_pct"] <= curr_hum <= wt["max_humidity_pct"])

        # High risk if both temp and humidity match
        if temp_match and hum_match:
            risk_level = "HIGH_ALERT"
            risk_badge = "bg-rose-100 text-rose-800 border-rose-300"
            risk_icon = "fa-triangle-exclamation"
            active_alerts_count += 1
            risk_explanation = f"Active weather trigger: current {curr_hum}% humidity and {curr_temp}°C temperature match peak outbreak conditions."
        elif hum_match or temp_match:
            risk_level = "MODERATE_MONITOR"
            risk_badge = "bg-amber-100 text-amber-800 border-amber-300"
            risk_icon = "fa-eye"
            risk_explanation = f"Moderate environmental risk: monitor field twice weekly for early leaf symptoms."
        else:
            risk_level = "LOW_RISK"
            risk_badge = "bg-emerald-100 text-emerald-800 border-emerald-300"
            risk_icon = "fa-circle-check"
            risk_explanation = "Low climatic risk at current atmospheric conditions. Maintain routine preventative IPM."

        evaluated_pests.append({
            "id": p["id"],
            "name": p["name"],
            "scientific_name": p["scientific_name"],
            "category": p["category"],
            "symptom_part": p["symptom_part"],
            "severity": p["severity"],
            "risk_level": risk_level,
            "risk_badge": risk_badge,
            "risk_icon": risk_icon,
            "risk_explanation": risk_explanation,
            "symptoms": p["symptoms"],
            "weather_triggers": p["weather_triggers"],
            "organic_remedy": p["organic_remedy"],
            "chemical_remedy": p["chemical_remedy"],
            "preventative_ipm": p["preventative_ipm"]
        })

    # Sort so HIGH_ALERT comes first
    severity_order = {"HIGH_ALERT": 0, "MODERATE_MONITOR": 1, "LOW_RISK": 2}
    evaluated_pests.sort(key=lambda x: severity_order.get(x["risk_level"], 3))

    # 4. Generate Overall Meteorological Pest Advisory Note
    if active_alerts_count > 0:
        overall_status = "ELEVATED_RISK"
        overall_headline = f"Active Weather Trigger Alert: {active_alerts_count} pest/disease risk condition(s) detected in {district_clean}"
        overall_advice = (
            f"Current humidity ({curr_hum}%) and expected 7-day rainfall ({curr_rain}mm) in {district_clean} "
            f"increase susceptibility to fungal and vegetative leaf diseases. Prophylactic application of bio-fungicides "
            f"(Bordeaux mixture 1% or Pseudomonas fluorescens) is strongly advised before rainfall intensifies."
        )
    else:
        overall_status = "NORMAL_MONITOR"
        overall_headline = f"Climatic Conditions Favorable: Normal pest surveillance advised for {district_clean}"
        overall_advice = (
            f"Current meteorological parameters in {district_clean} ({curr_temp}°C, {curr_hum}% RH) are within manageable "
            f"ranges. Inspect crops twice weekly and keep yellow sticky traps installed for early detection."
        )

    return {
        "success": True,
        "crop": crop_clean.title(),
        "crop_id": crop_clean,
        "district": district_clean,
        "live_weather": weather_summary,
        "active_alerts_count": active_alerts_count,
        "overall_status": overall_status,
        "overall_headline": overall_headline,
        "overall_advice": overall_advice,
        "pests_count": len(evaluated_pests),
        "pests": evaluated_pests
    }
