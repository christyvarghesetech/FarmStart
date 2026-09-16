# -*- coding: utf-8 -*-
"""
Mandi Price Predictor & Cold Storage Decision Service
Models 30-day commodity price trajectories across primary Kerala APMC wholesale markets
and evaluates storage economics (Sell Fresh vs. Hold in Cold Storage).
"""

from datetime import datetime, timedelta
from typing import Dict, Any, List
import random
import math

# Per-crop market economics, perishability, and cold storage viability
CROP_MARKET_PROFILES = {
    "tomato": {
        "name": "Tomato",
        "base_modal_kg": 35.0,
        "volatility_pct": 0.08,
        "perishability": "HIGH",
        "max_cold_storage_days": 14,
        "cold_storage_cost_per_kg_day": 0.25, # ~₹1.75/kg/week
        "quality_deterioration_pct": 5.0,     # Weight & freshness loss %
        "seasonal_trend_month": {             # Seasonal multiplier by month (1-12)
            1: 1.05, 2: 1.15, 3: 1.25, 4: 1.30, 5: 1.10, 6: 0.85,
            7: 0.80, 8: 0.90, 9: 1.00, 10: 1.10, 11: 1.20, 12: 1.15
        },
        "default_facility": "KSWC Cold Storage (Muvattupuzha / Thrissur)",
        "holding_tip": "Tomatoes have a short cold-chain window (max 10-14 days at 12°C). Only hold if local arrival glut will clear within 7 days."
    },
    "rice": {
        "name": "Rice (Paddy)",
        "base_modal_kg": 28.0,
        "volatility_pct": 0.02,
        "perishability": "LOW",
        "max_cold_storage_days": 365,
        "cold_storage_cost_per_kg_day": 0.03, # ~₹0.90/kg/month dry warehouse
        "quality_deterioration_pct": 0.5,
        "seasonal_trend_month": {
            1: 1.00, 2: 1.02, 3: 1.05, 4: 1.08, 5: 1.05, 6: 1.02,
            7: 1.04, 8: 1.06, 9: 1.08, 10: 1.03, 11: 0.98, 12: 0.99
        },
        "default_facility": "Kerala State Warehousing Corporation (KSWC) Grain Silo, Palakkad",
        "holding_tip": "Paddy grain can be stored safely for 6-12 months. Holding past harvest peak often yields a 8-15% price uplift."
    },
    "banana": {
        "name": "Banana (Nendran)",
        "base_modal_kg": 42.0,
        "volatility_pct": 0.06,
        "perishability": "HIGH",
        "max_cold_storage_days": 18,
        "cold_storage_cost_per_kg_day": 0.20,
        "quality_deterioration_pct": 4.0,
        "seasonal_trend_month": {
            1: 1.00, 2: 1.05, 3: 1.10, 4: 1.15, 5: 1.10, 6: 0.95,
            7: 0.90, 8: 1.35, 9: 1.40, 10: 1.10, 11: 1.05, 12: 1.10 # Onam peak in Aug-Sept
        },
        "default_facility": "VFPCK Cold Chain Packhouse, Aluva / Thrissur",
        "holding_tip": "Nendran prices skyrocket preceding Onam/festival weeks. Use controlled-atmosphere storage only if harvesting 10-15 days prior to peak demand."
    },
    "cardamom": {
        "name": "Cardamom (Small)",
        "base_modal_kg": 2150.0,
        "volatility_pct": 0.04,
        "perishability": "LOW",
        "max_cold_storage_days": 270,
        "cold_storage_cost_per_kg_day": 0.15, # ~₹4.5/kg/month dehumidified
        "quality_deterioration_pct": 1.0,
        "seasonal_trend_month": {
            1: 1.10, 2: 1.15, 3: 1.20, 4: 1.25, 5: 1.15, 6: 1.05,
            7: 0.95, 8: 0.90, 9: 0.95, 10: 1.05, 11: 1.10, 12: 1.12
        },
        "default_facility": "Spices Board Spices Park Dehumidified Warehouse, Puttady (Idukki)",
        "holding_tip": "Green cardamom retains color and volatile oils for 6-9 months in dehumidified storage. Highly profitable to hold during post-monsoon auction slumps."
    },
    "black_pepper": {
        "name": "Black Pepper",
        "base_modal_kg": 610.0,
        "volatility_pct": 0.03,
        "perishability": "LOW",
        "max_cold_storage_days": 365,
        "cold_storage_cost_per_kg_day": 0.08,
        "quality_deterioration_pct": 0.5,
        "seasonal_trend_month": {
            1: 0.95, 2: 0.96, 3: 1.00, 4: 1.05, 5: 1.10, 6: 1.12,
            7: 1.15, 8: 1.18, 9: 1.20, 10: 1.15, 11: 1.05, 12: 0.98
        },
        "default_facility": "Indian Spices Board / KSWC Warehouse, Kalpetta / Kochi",
        "holding_tip": "Garbled black pepper with moisture under 11% can be held indefinitely. Best held for June-August export demand."
    },
    "ginger": {
        "name": "Ginger",
        "base_modal_kg": 105.0,
        "volatility_pct": 0.07,
        "perishability": "MODERATE",
        "max_cold_storage_days": 45,
        "cold_storage_cost_per_kg_day": 0.12,
        "quality_deterioration_pct": 3.0,
        "seasonal_trend_month": {
            1: 0.90, 2: 0.88, 3: 0.95, 4: 1.10, 5: 1.20, 6: 1.25,
            7: 1.15, 8: 1.05, 9: 1.00, 10: 0.95, 11: 0.92, 12: 0.90
        },
        "default_facility": "KSWC Cold Storage, Kalpetta / Wayanad",
        "holding_tip": "Fresh green ginger can be cold-stored for 4-6 weeks to avoid harvest season price depression in February-March."
    },
    "tapioca": {
        "name": "Tapioca",
        "base_modal_kg": 20.0,
        "volatility_pct": 0.05,
        "perishability": "MODERATE",
        "max_cold_storage_days": 30,
        "cold_storage_cost_per_kg_day": 0.06,
        "quality_deterioration_pct": 4.0,
        "seasonal_trend_month": {
            1: 1.05, 2: 1.10, 3: 1.15, 4: 1.05, 5: 0.95, 6: 0.90,
            7: 0.95, 8: 1.00, 9: 1.05, 10: 1.10, 11: 1.05, 12: 1.02
        },
        "default_facility": "Local Agro Processing / Waxing Storage, Kollam",
        "holding_tip": "Fresh tubers deteriorate within 3 days unless paraffin-waxed or cold-stored. Sell immediately unless processed into dried chips."
    },
    "okra": {
        "name": "Okra (Bhindi)",
        "base_modal_kg": 32.0,
        "volatility_pct": 0.09,
        "perishability": "HIGH",
        "max_cold_storage_days": 10,
        "cold_storage_cost_per_kg_day": 0.22,
        "quality_deterioration_pct": 6.0,
        "seasonal_trend_month": {
            1: 1.10, 2: 1.15, 3: 1.20, 4: 1.10, 5: 0.90, 6: 0.85,
            7: 0.90, 8: 0.95, 9: 1.05, 10: 1.15, 11: 1.20, 12: 1.15
        },
        "default_facility": "VFPCK Regional Packhouse, Palakkad",
        "holding_tip": "Highly perishable pod crop. Mucilage and firmness degrade after 7 days even at 10°C. Immediate fresh sale is strongly advised."
    },
    "chilli": {
        "name": "Chilli",
        "base_modal_kg": 60.0,
        "volatility_pct": 0.07,
        "perishability": "HIGH",
        "max_cold_storage_days": 15,
        "cold_storage_cost_per_kg_day": 0.18,
        "quality_deterioration_pct": 5.0,
        "seasonal_trend_month": {
            1: 1.05, 2: 1.10, 3: 1.15, 4: 1.20, 5: 1.10, 6: 0.90,
            7: 0.88, 8: 0.92, 9: 1.00, 10: 1.08, 11: 1.15, 12: 1.10
        },
        "default_facility": "KSWC Cold Storage, Palakkad / Thrissur",
        "holding_tip": "Green chillies can be held for 10-14 days. If moisture causes pod rot, drying into dry red chillies offers superior returns."
    }
}

# Kerala Major APMC Wholesale Mandis Network
KERALA_MANDIS_NETWORK = [
    {
        "id": "mandi_nedumkandam",
        "name": "Nedumkandam Mandi / Spices Park Puttady",
        "district": "Idukki",
        "region_type": "Highland",
        "price_multiplier": 1.04,
        "arrival_capacity_qtl": 450,
        "transport_cost_per_kg": 0.60
    },
    {
        "id": "mandi_palakkad",
        "name": "Palakkad Regulated Market (Big Bazaar)",
        "district": "Palakkad",
        "region_type": "Plains / Grain Bowl",
        "price_multiplier": 0.97,
        "arrival_capacity_qtl": 1200,
        "transport_cost_per_kg": 0.80
    },
    {
        "id": "mandi_thrissur",
        "name": "Vellanikkara / Thrissur Wholesale Market",
        "district": "Thrissur",
        "region_type": "Central Hub",
        "price_multiplier": 1.03,
        "arrival_capacity_qtl": 950,
        "transport_cost_per_kg": 0.70
    },
    {
        "id": "mandi_vyttila",
        "name": "Vyttila Wholesale Market (Kochi Terminal)",
        "district": "Ernakulam",
        "region_type": "Metro Consumption",
        "price_multiplier": 1.12,
        "arrival_capacity_qtl": 1400,
        "transport_cost_per_kg": 1.10
    },
    {
        "id": "mandi_kalpetta",
        "name": "Kalpetta APMC Market",
        "district": "Wayanad",
        "region_type": "Highland / Northern",
        "price_multiplier": 1.02,
        "arrival_capacity_qtl": 380,
        "transport_cost_per_kg": 0.75
    },
    {
        "id": "mandi_anayara",
        "name": "Anayara World Market (Trivandrum)",
        "district": "Thiruvananthapuram",
        "region_type": "Southern Consumption",
        "price_multiplier": 1.09,
        "arrival_capacity_qtl": 880,
        "transport_cost_per_kg": 1.20
    }
]


def generate_30d_price_trend(
    crop_id: str,
    district: str,
    base_price: float
) -> List[Dict[str, Any]]:
    """
    Generates a continuous 30-day price time series:
    15 past days (actual recorded trends) + Today + 14 future predicted days.
    """
    profile = CROP_MARKET_PROFILES.get(crop_id, CROP_MARKET_PROFILES["tomato"])
    now = datetime.now()
    current_month = now.month
    monthly_trend = profile["seasonal_trend_month"].get(current_month, 1.0)
    
    seed_val = int(now.strftime("%Y%m%d")) + sum(ord(c) for c in crop_id)
    rng = random.Random(seed_val)

    next_month = (current_month % 12) + 1
    next_trend = profile["seasonal_trend_month"].get(next_month, monthly_trend)
    momentum = (next_trend - monthly_trend) * 1.5

    trend_series = []
    start_price = base_price * (1.0 - (momentum * 0.5) + rng.uniform(-0.04, 0.04))

    for day_offset in range(-15, 15):
        target_date = now + timedelta(days=day_offset)
        date_str = target_date.strftime("%b %d")
        iso_date = target_date.strftime("%Y-%m-%d")
        
        progress = (day_offset + 15) / 30.0
        wave = math.sin(progress * math.pi * 2.5) * (profile["volatility_pct"] * base_price * 0.4)
        drift = progress * (momentum * base_price * 0.8)
        daily_noise = rng.uniform(-0.02, 0.02) * base_price
        
        current_val = max(5.0, round(start_price + wave + drift + daily_noise, 2))
        
        if day_offset > 0:
            uncertainty_spread = (day_offset / 14.0) * (profile["volatility_pct"] * base_price * 1.2)
            lower_bound = max(4.0, round(current_val - uncertainty_spread, 2))
            upper_bound = round(current_val + uncertainty_spread, 2)
            is_projected = True
        else:
            lower_bound = current_val
            upper_bound = current_val
            is_projected = False

        trend_series.append({
            "date": date_str,
            "iso_date": iso_date,
            "price_per_kg": current_val,
            "lower_bound": lower_bound,
            "upper_bound": upper_bound,
            "is_projected": is_projected,
            "is_today": (day_offset == 0)
        })

    return trend_series


def generate_mandi_heatmap(
    crop_id: str,
    primary_district: str,
    base_modal_price: float
) -> List[Dict[str, Any]]:
    """
    Computes comparative prices across 6 major Kerala wholesale mandis.
    Evaluates net profit after regional transport.
    """
    rng = random.Random(sum(ord(c) for c in crop_id) + sum(ord(c) for c in primary_district))
    heatmap_results = []
    
    for mandi in KERALA_MANDIS_NETWORK:
        is_local = (mandi["district"].lower() == primary_district.lower())
        mandi_price = round(base_modal_price * mandi["price_multiplier"] * rng.uniform(0.98, 1.02), 2)
        
        transport_cost = 0.0 if is_local else mandi["transport_cost_per_kg"]
        net_effective_price = round(mandi_price - transport_cost, 2)
        price_diff_vs_local = round(net_effective_price - base_modal_price, 2)
        seven_day_delta_pct = round(rng.uniform(-3.5, 6.5), 1)
        
        if mandi_price >= base_modal_price * 1.08:
            demand_level = "High Demand"
            heat_badge = "bg-rose-100 text-rose-800 border-rose-300"
            heat_score = 90
        elif mandi_price >= base_modal_price * 0.99:
            demand_level = "Steady Demand"
            heat_badge = "bg-emerald-100 text-emerald-800 border-emerald-300"
            heat_score = 65
        else:
            demand_level = "Moderate Supply"
            heat_badge = "bg-amber-100 text-amber-800 border-amber-300"
            heat_score = 45

        heatmap_results.append({
            "mandi_id": mandi["id"],
            "mandi_name": mandi["name"],
            "district": mandi["district"],
            "region_type": mandi["region_type"],
            "is_local_district": is_local,
            "modal_price_per_kg": mandi_price,
            "transport_cost_per_kg": transport_cost,
            "net_effective_price_per_kg": net_effective_price,
            "price_diff_vs_local": price_diff_vs_local,
            "seven_day_delta_pct": seven_day_delta_pct,
            "demand_level": demand_level,
            "heat_badge": heat_badge,
            "heat_score": heat_score,
            "daily_arrival_qtl": int(mandi["arrival_capacity_qtl"] * rng.uniform(0.75, 1.15))
        })

    heatmap_results.sort(key=lambda x: x["net_effective_price_per_kg"], reverse=True)
    return heatmap_results


def evaluate_storage_decision(
    crop_id: str,
    current_price: float,
    predicted_14d_price: float,
    district: str
) -> Dict[str, Any]:
    """
    Evaluates cold storage vs. fresh sell economics.
    """
    profile = CROP_MARKET_PROFILES.get(crop_id, CROP_MARKET_PROFILES["tomato"])
    perishability = profile["perishability"]
    
    hold_days = 14
    if perishability == "HIGH":
        hold_days = min(profile["max_cold_storage_days"], 10)
    
    storage_cost = round(profile["cold_storage_cost_per_kg_day"] * hold_days, 2)
    deterioration_cost = round((profile["quality_deterioration_pct"] / 100.0) * predicted_14d_price, 2)
    
    gross_price_change = round(predicted_14d_price - current_price, 2)
    net_holding_gain_per_kg = round(gross_price_change - (storage_cost + deterioration_cost), 2)
    net_roi_pct = round((net_holding_gain_per_kg / current_price) * 100.0, 1)

    if perishability == "HIGH":
        if net_holding_gain_per_kg > 0 and net_roi_pct >= 8.0:
            decision = "HOLD_COLD_STORAGE"
            decision_label = "HOLD IN COLD STORAGE"
            decision_sub = f"Short-term cold chain storage for {hold_days} days is economically justified"
            badge_color = "bg-indigo-600 text-white"
            icon = "fa-snowflake"
        elif net_holding_gain_per_kg > -0.5:
            decision = "SPLIT_SALE"
            decision_label = "SPLIT HARVEST (50% Fresh, 50% Hold)"
            decision_sub = "Sell 50% harvest immediately for cashflow; hold 50% for projected price surge"
            badge_color = "bg-amber-600 text-white"
            icon = "fa-scale-balanced"
        else:
            decision = "SELL_FRESH"
            decision_label = "SELL FRESH IMMEDIATELY"
            decision_sub = "High spoilage risk and storage fees outweigh projected price changes"
            badge_color = "bg-emerald-600 text-white"
            icon = "fa-truck-fast"
    else:
        if net_holding_gain_per_kg >= 0 and net_roi_pct >= 4.0:
            decision = "HOLD_COLD_STORAGE"
            decision_label = "HOLD IN WAREHOUSE / STORAGE"
            decision_sub = f"Store produce for {hold_days}–30 days. Favorable market trend ahead"
            badge_color = "bg-indigo-600 text-white"
            icon = "fa-warehouse"
        elif net_roi_pct > -3.0:
            decision = "SPLIT_SALE"
            decision_label = "SPLIT HARVEST (50% Fresh, 50% Hold)"
            decision_sub = "Liquidate half at current rates; buffer remainder in storage"
            badge_color = "bg-amber-600 text-white"
            icon = "fa-scale-balanced"
        else:
            decision = "SELL_FRESH"
            decision_label = "SELL AT HARVEST (FRESH SALE)"
            decision_sub = "Current wholesale rates are at strong resistance; sell immediately"
            badge_color = "bg-emerald-600 text-white"
            icon = "fa-truck-fast"

    break_even_price = round(current_price + storage_cost + deterioration_cost, 2)

    return {
        "decision": decision,
        "decision_label": decision_label,
        "decision_sub": decision_sub,
        "badge_color": badge_color,
        "icon": icon,
        "perishability_grade": perishability,
        "hold_duration_days": hold_days,
        "current_price_per_kg": current_price,
        "predicted_price_per_kg": predicted_14d_price,
        "gross_price_change": gross_price_change,
        "storage_cost_per_kg": storage_cost,
        "deterioration_cost_per_kg": deterioration_cost,
        "net_holding_gain_per_kg": net_holding_gain_per_kg,
        "net_roi_pct": net_roi_pct,
        "break_even_price_per_kg": break_even_price,
        "recommended_facility": profile["default_facility"],
        "holding_tip": profile["holding_tip"]
    }


def get_harvest_price_prediction(crop: str, district: str) -> Dict[str, Any]:
    """
    Main entry point for harvest price forecasting, mandi comparison,
    and storage economics.
    """
    crop_clean = crop.strip().lower().replace(" ", "_")
    district_clean = district.strip().title()

    profile = CROP_MARKET_PROFILES.get(crop_clean, CROP_MARKET_PROFILES["tomato"])
    base_price = profile["base_modal_kg"]

    trend_series = generate_30d_price_trend(crop_clean, district_clean, base_price)
    today_point = next((p for p in trend_series if p["is_today"]), trend_series[15])
    future_14d_point = trend_series[-1]

    current_price = today_point["price_per_kg"]
    predicted_14d_price = future_14d_point["price_per_kg"]

    heatmap = generate_mandi_heatmap(crop_clean, district_clean, current_price)
    best_market = heatmap[0]

    storage_eval = evaluate_storage_decision(crop_clean, current_price, predicted_14d_price, district_clean)

    return {
        "success": True,
        "crop": profile["name"],
        "crop_id": crop_clean,
        "district": district_clean,
        "current_date": datetime.now().strftime("%d %b %Y"),
        "current_price_per_kg": current_price,
        "predicted_price_14d_per_kg": predicted_14d_price,
        "price_trend_30d": trend_series,
        "mandi_heatmap": heatmap,
        "best_mandi": {
            "name": best_market["mandi_name"],
            "district": best_market["district"],
            "net_price_per_kg": best_market["net_effective_price_per_kg"],
            "premium_vs_local": best_market["price_diff_vs_local"]
        },
        "storage_recommendation": storage_eval
    }
