from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.advisory import (
    WeatherAdvisoryRequest,
    WeatherAdvisoryResponse,
    AdvisoryChatRequest,
    AdvisoryChatResponse,
    AdvisoryChatContext
)
from app.services.weather_service import get_weather_forecast
from app.services.sowing_service import evaluate_sowing_advisory
from app.services.llm_service import generate_llm_advisory

router = APIRouter(tags=["Advisory"])


@router.post(
    "/weather-advisory",
    response_model=WeatherAdvisoryResponse,
    summary="Weather-aware sowing window advisory"
)
async def get_weather_advisory(
    payload: WeatherAdvisoryRequest,
    db: Session = Depends(get_db)
):
    """
    Returns optimal sowing window, upcoming weather conditions, and safe/unsafe alert
    based on live/regional forecast and crop calendar.
    """
    try:
        # 1. Fetch weather forecast (live OpenWeatherMap or high-res agro-meteorological model)
        forecast = await get_weather_forecast(
            district=payload.district,
            lat=payload.lat,
            lon=payload.lon
        )

        # 2. Evaluate against crop and district rules
        advisory = evaluate_sowing_advisory(
            crop_id=payload.crop,
            district=payload.district,
            forecast=forecast,
            db=db
        )

        return advisory

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate weather advisory: {str(e)}"
        )


@router.post(
    "/advisory-chat",
    response_model=AdvisoryChatResponse,
    summary="LLM conversational explainer and farmer Q&A"
)
async def advisory_chat(
    payload: AdvisoryChatRequest
):
    """
    Accepts farmer's natural-language question with structured context
    (ML suitability score, weather advisory, and seed prices) and returns
    an empathetic, plain-language advisory with actionable tips.
    """
    try:
        ctx = payload.context or AdvisoryChatContext()
        farmer = payload.farmer_name or "Farmer"

        response = generate_llm_advisory(
            farmer_name=farmer,
            question=payload.question,
            context=ctx,
            conversation_history=payload.conversation_history
        )

        return response

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Advisory chat agent error: {str(e)}"
        )
