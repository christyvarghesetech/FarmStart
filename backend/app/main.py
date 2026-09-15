from fastapi import FastAPI, Depends, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from sqlalchemy.orm import Session
from app.config import settings
from app.database import Base, engine, get_db
from app.routers import advisory_router, suitability_router, prices_router, schemes_router
from app.services.ml_service import get_model, score_crop_suitability
from app.services.weather_service import get_weather_forecast
from app.services.sowing_service import evaluate_sowing_advisory
from app.services.llm_service import generate_llm_advisory
from app.schemas.advisory import AdvisoryChatContext
from app.models import SeedPrice
import os


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Ensure DB tables exist
    Base.metadata.create_all(bind=engine)
    # Pre-warm ML model
    try:
        get_model()
        print("FarmStart ML suitability model loaded successfully.")
    except Exception as e:
        print(f"Warning: ML model warmup failed: {e}")
    yield
    # Shutdown
    print("FarmStart backend shutting down.")


app = FastAPI(
    title="FarmStart API (New Farmer Copilot)",
    description=(
        "AI-powered agricultural decision-support copilot for new and first-time farmers in Kerala. "
        "Integrates live weather forecasting, scikit-learn ML suitability scoring, fair seed price benchmarks, "
        "and Groq LLM plain-language conversational advisory."
    ),
    version="1.0.0",
    lifespan=lifespan
)

# Enable CORS for React and mobile clients
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(advisory_router)
app.include_router(suitability_router)
app.include_router(prices_router)
app.include_router(schemes_router)

# Mount frontend UI if available
_frontend_candidates = [
    os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "frontend")),
    os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "farmstart-frontend")),
]
FRONTEND_DIR = next((p for p in _frontend_candidates if os.path.exists(p)), None)
if FRONTEND_DIR:
    app.mount("/app", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")


@app.get("/", summary="Health Check and API Metadata")
def root():
    return {
        "project": "FarmStart (New Farmer Copilot)",
        "track": "Agriculture - AI Conclave 2026",
        "status": "online",
        "version": "1.0.0",
        "docs_url": "/docs",
        "endpoints": [
            "POST /weather-advisory",
            "POST /suitability-score",
            "POST /advisory-chat",
            "GET /seed-price-check",
            "GET /crop-fit",
            "GET /government-schemes",
            "POST /full-advisory"
        ]
    }


@app.post("/full-advisory", summary="Complete end-to-end copilot advisory (All-in-one)")
async def full_advisory(
    farmer_name: str = "Farmer",
    district: str = "Idukki",
    crop: str = "tomato",
    question: str = None,
    db: Session = Depends(get_db)
):
    """
    Combines weather forecast, ML suitability scoring, seed price lookup,
    and conversational LLM explanation into a single unified payload for the frontend.
    """
    if not question:
        crop_clean = crop.replace('_', ' ')
        question = f"Is it a good time to cultivate {crop_clean} in {district} right now?"
    try:
        # 1. Weather forecast
        forecast = await get_weather_forecast(district=district)

        # 2. Sowing window evaluation
        sowing = evaluate_sowing_advisory(
            crop_id=crop,
            district=district,
            forecast=forecast,
            db=db
        )

        # 3. ML Suitability Scoring
        suitability = score_crop_suitability(
            crop=crop,
            district=district
        )

        # 4. Seed price benchmark
        price_rec = db.query(SeedPrice).filter(
            SeedPrice.crop_id == crop.strip().lower(),
            SeedPrice.region == district.strip().title()
        ).first()

        if not price_rec:
            price_rec = db.query(SeedPrice).filter(
                SeedPrice.crop_id == crop.strip().lower()
            ).first()

        price_str = (
            f"₹{price_rec.min_price:.0f} - ₹{price_rec.max_price:.0f} ({price_rec.unit})"
            if price_rec else "₹350 - ₹450 / 100g"
        )

        # 5. Build LLM Context & Generate Advisory
        ctx = AdvisoryChatContext(
            district=district,
            crop=crop,
            soil_type=suitability.get("soil_type", "Laterite soil"),
            suitability_score=suitability.get("suitability_score", 85.0),
            suitability_category=suitability.get("suitability_category", "High"),
            is_safe_to_sow=sowing.get("is_safe_to_sow", True),
            seed_price_range=price_str,
            weather_forecast=f"{forecast.get('weather_condition', 'Pleasant')}, {forecast.get('avg_temp_c', 23.5)}°C, ~{forecast.get('total_rainfall_next_7d_mm', 30.0)}mm rain"
        )

        llm_response = generate_llm_advisory(
            farmer_name=farmer_name,
            question=question,
            context=ctx
        )

        return {
            "success": True,
            "farmer": {
                "name": farmer_name,
                "district": district,
                "crop": crop
            },
            "weather_advisory": sowing,
            "ml_suitability": suitability,
            "seed_price_benchmark": {
                "range": price_str,
                "details": {
                    "min_price": price_rec.min_price if price_rec else 350.0,
                    "max_price": price_rec.max_price if price_rec else 450.0,
                    "modal_price": price_rec.modal_price if price_rec else 390.0,
                    "source": price_rec.source if price_rec else "KSSDA"
                } if price_rec else None
            },
            "copilot_chat": llm_response
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Full advisory generation error: {str(e)}"
        )
