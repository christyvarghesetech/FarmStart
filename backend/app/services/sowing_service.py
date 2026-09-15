from datetime import datetime
from typing import Dict, Any, List
from sqlalchemy.orm import Session
from app.models import SowingWindow, Crop
from app.schemas.advisory import SowingWindowDetail


def evaluate_sowing_advisory(
    crop_id: str,
    district: str,
    forecast: Dict[str, Any],
    db: Session
) -> Dict[str, Any]:
    """
    Rule-based engine combining upcoming weather forecast and regional crop calendars
    to calculate safe sowing window and risk factors.
    """
    crop_clean = crop_id.strip().lower().replace(" ", "_")
    district_clean = district.strip().title()

    # Query calendar for specific district or fallback to General
    window_record = db.query(SowingWindow).filter(
        SowingWindow.crop_id == crop_clean,
        SowingWindow.region == district_clean
    ).first()

    if not window_record:
        window_record = db.query(SowingWindow).filter(
            SowingWindow.crop_id == crop_clean
        ).first()

    crop_record = db.query(Crop).filter(Crop.id == crop_clean).first()

    now = datetime.now()
    current_month_day = now.strftime("%m-%d")

    season_name = "Recommended Sowing Season"
    start_str = "09-15"
    end_str = "11-30"
    sowing_tips = "Plant healthy seedlings in well-drained raised beds."
    safe_rain_max = 220.0
    safe_temp_min = 16.0
    safe_temp_max = 32.0

    if window_record:
        season_name = window_record.season_name or season_name
        start_str = window_record.recommended_start
        end_str = window_record.recommended_end
        sowing_tips = window_record.sowing_tips or sowing_tips
        safe_rain_max = window_record.safe_rainfall_max_mm or safe_rain_max
        safe_temp_min = window_record.safe_temp_min_c or safe_temp_min
        safe_temp_max = window_record.safe_temp_max_c or safe_temp_max
    elif crop_record:
        season_name = crop_record.sowing_season

    # Check date window
    is_in_window = True
    if len(start_str) == 5 and len(end_str) == 5:
        if start_str <= end_str:
            is_in_window = (start_str <= current_month_day <= end_str)
        else: # wraps around year end
            is_in_window = (current_month_day >= start_str or current_month_day <= end_str)

    # Risk evaluation
    risk_factors: List[str] = []
    total_rain_7d = forecast.get("total_rainfall_next_7d_mm", 30.0)
    avg_temp = forecast.get("avg_temp_c", 24.0)
    rain_prob = forecast.get("rain_probability_pct", 50)

    # 1. Rain intensity risk
    if total_rain_7d > 120.0 or rain_prob > 85:
        risk_factors.append(
            f"Heavy rainfall predicted ({total_rain_7d} mm in 7 days). Seedlings risk wash-out or damping off."
        )
    elif total_rain_7d < 10.0 and rain_prob < 20:
        risk_factors.append(
            "Dry spell forecast. Supplemental nursery watering or drip irrigation will be critical."
        )

    # 2. Temperature tolerance risk
    if avg_temp < safe_temp_min:
        risk_factors.append(
            f"Average forecast temperature ({avg_temp}°C) is below optimal threshold ({safe_temp_min}°C). Germination may be delayed."
        )
    elif avg_temp > safe_temp_max:
        risk_factors.append(
            f"High heat forecast ({avg_temp}°C) may stress tender germinating seeds."
        )

    # Determine safety status
    if not is_in_window and len(risk_factors) >= 2:
        safety_status = "NOT_RECOMMENDED"
        is_safe = False
        advisory_notes = (
            f"Currently outside optimal regional sowing window for {crop_clean.title()} in {district_clean}, "
            f"with unfavorable weather conditions. Delay sowing until the next cycle."
        )
    elif risk_factors:
        safety_status = "CAUTION"
        is_safe = True
        advisory_notes = (
            f"Favorable sowing window is active, but caution is advised due to upcoming weather conditions. "
            f"{' '.join(risk_factors)} Follow protective field measures like raised beds or mulching."
        )
    else:
        safety_status = "SAFE_TO_SOW"
        is_safe = True
        advisory_notes = (
            f"Excellent conditions! Current forecast ({avg_temp}°C, {total_rain_7d} mm rain) aligns perfectly "
            f"with the {season_name} for {crop_clean.title()} in {district_clean}."
        )

    window_detail = SowingWindowDetail(
        season_name=season_name,
        recommended_start=start_str,
        recommended_end=end_str,
        is_currently_in_window=is_in_window,
        sowing_tips=sowing_tips
    )

    return {
        "crop": crop_clean.title(),
        "district": district_clean,
        "is_safe_to_sow": is_safe,
        "safety_status": safety_status,
        "recommended_window": window_detail,
        "forecast_summary": forecast,
        "risk_factors": risk_factors,
        "advisory_notes": advisory_notes
    }
