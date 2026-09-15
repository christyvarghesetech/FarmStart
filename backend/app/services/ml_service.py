import os
import joblib
import numpy as np
import pandas as pd
from typing import Dict, Any, List
from app.data.seed_data import KERALA_DISTRICTS, CROPS_CATALOG

MODEL_PATH = os.path.join(
    os.path.dirname(__file__), "..", "data", "ml_models", "suitability_model.pkl"
)

# Load model bundle once at startup
_model_bundle = None

def get_model():
    global _model_bundle
    if _model_bundle is None:
        if os.path.exists(MODEL_PATH):
            _model_bundle = joblib.load(MODEL_PATH)
        else:
            raise RuntimeError(f"Suitability model file not found at {MODEL_PATH}")
    return _model_bundle


def score_crop_suitability(
    crop: str,
    district: str,
    soil_type: str = None,
    nitrogen: float = None,
    phosphorus: float = None,
    potassium: float = None,
    ph: float = None,
    temperature: float = None,
    humidity: float = None,
    rainfall: float = None
) -> Dict[str, Any]:
    """
    ML scoring of crop suitability based on trained scikit-learn model.
    """
    bundle = get_model()
    model = bundle["model"]
    feature_cols = bundle["feature_cols"]
    crop_enc = bundle["crop_encoder"]
    district_enc = bundle["district_encoder"]
    soil_enc = bundle["soil_encoder"]
    classes = bundle["classes"]

    crop_clean = crop.strip().lower().replace(" ", "_")
    district_clean = district.strip().title()

    # Get district baseline defaults for any missing inputs
    dist_meta = KERALA_DISTRICTS.get(district_clean, KERALA_DISTRICTS["Idukki"])
    
    resolved_soil = soil_type if soil_type else dist_meta["primary_soil"].split("&")[0].split("/")[0].strip()
    resolved_n = nitrogen if nitrogen is not None else dist_meta["default_npk"]["N"]
    resolved_p = phosphorus if phosphorus is not None else dist_meta["default_npk"]["P"]
    resolved_k = potassium if potassium is not None else dist_meta["default_npk"]["K"]
    resolved_ph = ph if ph is not None else dist_meta["default_npk"]["ph"]
    resolved_temp = temperature if temperature is not None else 23.5
    resolved_humidity = humidity if humidity is not None else 78.0
    resolved_rain = rainfall if rainfall is not None else 180.0

    # Safely transform categorical variables
    def safe_transform(encoder, val, fallback=0):
        if val in encoder.classes_:
            return int(encoder.transform([val])[0])
        return fallback

    c_val = safe_transform(crop_enc, crop_clean, 0)
    d_val = safe_transform(district_enc, district_clean, 0)
    s_val = safe_transform(soil_enc, resolved_soil, 0)

    input_df = pd.DataFrame([{
        "crop_enc": c_val,
        "district_enc": d_val,
        "soil_enc": s_val,
        "ph": resolved_ph,
        "nitrogen": resolved_n,
        "phosphorus": resolved_p,
        "potassium": resolved_k,
        "temperature": resolved_temp,
        "humidity": resolved_humidity,
        "rainfall": resolved_rain
    }])[feature_cols]

    # Predict class & probabilities
    prediction = model.predict(input_df)[0]
    probabilities = model.predict_proba(input_df)[0]
    prob_dict = {cls_name: round(float(prob), 4) for cls_name, prob in zip(classes, probabilities)}

    pred_idx = list(classes).index(prediction)
    confidence = round(float(probabilities[pred_idx]) * 100, 1)

    # Calculate 0-100 composite suitability score
    # High: 75-100, Medium: 50-74, Low: 10-49
    high_p = prob_dict.get("High", 0.0)
    med_p = prob_dict.get("Medium", 0.0)
    low_p = prob_dict.get("Low", 0.0)

    composite_score = round(float(high_p * 92.0 + med_p * 65.0 + low_p * 35.0), 1)

    # Limiting factors identification
    limiting_factors: List[str] = []
    key_recommendations: List[str] = []

    # pH analysis
    if resolved_ph < 5.5:
        limiting_factors.append(f"Soil is strongly acidic (pH {resolved_ph:.1f}). Nutrient uptake will be restricted.")
        key_recommendations.append("Apply agricultural lime or dolomite (500 kg/ha) 2-3 weeks prior to planting.")
    elif resolved_ph > 7.5:
        limiting_factors.append(f"Soil is mildly alkaline (pH {resolved_ph:.1f}). Micronutrient availability may decrease.")
        key_recommendations.append("Incorporate well-decomposed organic matter and gypsum.")
    else:
        key_recommendations.append("Soil pH is in optimal range for nutrient absorption.")

    # Nutrient analysis
    if resolved_n < 50:
        limiting_factors.append(f"Available Nitrogen is low ({resolved_n:.0f} kg/ha).")
        key_recommendations.append("Apply neem-coated urea or enriched compost during basal manuring.")
    if resolved_k < 45:
        limiting_factors.append(f"Potassium level is below recommended range ({resolved_k:.0f} kg/ha).")
        key_recommendations.append("Apply Muriate of Potash (MOP) to boost pest resistance and fruit quality.")

    # Rain & humidity
    if resolved_rain > 250:
        limiting_factors.append(f"Monthly rainfall ({resolved_rain:.0f} mm) is high. Potential risk of fungal diseases.")
        key_recommendations.append("Drench root zone with Trichoderma viride and ensure deep drainage channels.")

    if not limiting_factors:
        limiting_factors.append("No critical agronomic inhibitors identified under current inputs.")
        key_recommendations.append("Maintain standard KAU package of practices with regular weeding and fertigation.")

    # Yield projection description
    if prediction == "High":
        yield_prediction = "Optimal expected yield (90% - 105% of regional benchmark)"
    elif prediction == "Medium":
        yield_prediction = "Moderate expected yield (70% - 85% of regional benchmark, improved with suggested soil amendments)"
    else:
        yield_prediction = "Low expected yield (<60% benchmark) - elevated environmental stress"

    return {
        "crop": crop_clean.title(),
        "district": district_clean,
        "soil_type": resolved_soil,
        "suitability_category": prediction,
        "suitability_score": composite_score,
        "ml_confidence_pct": confidence,
        "probabilities": prob_dict,
        "yield_prediction": yield_prediction,
        "limiting_factors": limiting_factors,
        "key_recommendations": key_recommendations,
        "soil_parameters_used": {
            "nitrogen": resolved_n,
            "phosphorus": resolved_p,
            "potassium": resolved_k,
            "ph": resolved_ph,
            "temperature": resolved_temp,
            "humidity": resolved_humidity,
            "rainfall": resolved_rain
        }
    }
