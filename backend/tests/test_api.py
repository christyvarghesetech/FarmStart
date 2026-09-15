import os
import sys
import pytest
from fastapi.testclient import TestClient

# Ensure app is importable
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from app.main import app
from app.database import Base, engine
from scripts.init_db import init_database

client = TestClient(app)


@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    init_database()
    yield


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["project"] == "FarmStart (New Farmer Copilot)"
    assert data["status"] == "online"


def test_weather_advisory_tomato_idukki():
    payload = {
        "crop": "tomato",
        "district": "Idukki"
    }
    response = client.post("/weather-advisory", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["crop"] == "Tomato"
    assert data["district"] == "Idukki"
    assert "is_safe_to_sow" in data
    assert "safety_status" in data
    assert "recommended_window" in data
    assert "forecast_summary" in data
    assert data["recommended_window"]["season_name"] is not None


def test_suitability_score_tomato():
    payload = {
        "crop": "tomato",
        "district": "Idukki",
        "soil_type": "Hill soil",
        "nitrogen": 80.0,
        "phosphorus": 45.0,
        "potassium": 65.0,
        "ph": 6.2,
        "temperature": 23.0,
        "humidity": 76.0,
        "rainfall": 170.0
    }
    response = client.post("/suitability-score", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["crop"] == "Tomato"
    assert data["district"] == "Idukki"
    assert data["suitability_category"] in ["High", "Medium", "Low"]
    assert 0 <= data["suitability_score"] <= 100
    assert "ml_confidence_pct" in data
    assert len(data["key_recommendations"]) > 0


def test_seed_price_check():
    response = client.get("/seed-price-check?crop=tomato&region=Idukki")
    assert response.status_code == 200
    data = response.json()
    assert data["crop"] == "Tomato"
    assert data["region"] == "Idukki"
    assert data["min_price"] <= data["modal_price"] <= data["max_price"]
    assert "KSSDA" in data["source"] or "e-NAM" in data["source"]
    assert len(data["varieties"]) > 0
    assert "produce_market_price" in data


def test_live_market_price():
    response = client.get("/live-market-price?crop=tomato&region=Idukki")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["crop"] == "Tomato"
    assert data["region"] == "Idukki"
    assert "primary_mandi" in data
    assert "produce_market_price" in data
    assert data["produce_market_price"]["modal_price_per_kg"] > 0
    assert data["seed_input_price"]["modal_price"] > 0


def test_crop_fit():
    response = client.get("/crop-fit?district=Idukki")
    assert response.status_code == 200
    data = response.json()
    assert data["district"] == "Idukki"
    assert len(data["suitable_crops"]) > 0
    # Tomato or Cardamom or Pepper should be in suitable crops
    crop_ids = [c["crop_id"] for c in data["suitable_crops"]]
    assert "tomato" in crop_ids
    assert "cardamom" in crop_ids


def test_government_schemes():
    response = client.get("/government-schemes?crop=tomato")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["count"] > 0
    # Subhiksha Keralam or PMFBY should be present
    scheme_ids = [s["id"] for s in data["schemes"]]
    assert "subhiksha-keralam" in scheme_ids or "pm-kisan" in scheme_ids


def test_advisory_chat_anil_narrative():
    payload = {
        "farmer_name": "Anil",
        "question": "Is it a good time to plant tomatoes here in Idukki?",
        "context": {
            "district": "Idukki",
            "crop": "tomato",
            "soil_type": "Hill soil",
            "suitability_score": 88.0,
            "suitability_category": "High",
            "is_safe_to_sow": True,
            "seed_price_range": "₹350 - ₹450 / 100g",
            "weather_forecast": "Pleasant with light afternoon rain, 23.5°C"
        }
    }
    response = client.post("/advisory-chat", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["farmer_name"] == "Anil"
    assert len(data["reply"]) > 20
    assert len(data["actionable_tips"]) >= 2
    assert len(data["suggested_followups"]) >= 1


def test_full_advisory_composite():
    response = client.post(
        "/full-advisory?farmer_name=Anil&district=Idukki&crop=tomato&question=Is%20it%20a%20good%20time%20to%20plant%20tomatoes%20here?"
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["farmer"]["name"] == "Anil"
    assert "weather_advisory" in data
    assert "ml_suitability" in data
    assert "seed_price_benchmark" in data
    assert "copilot_chat" in data
