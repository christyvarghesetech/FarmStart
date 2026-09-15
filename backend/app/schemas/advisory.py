from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class WeatherAdvisoryRequest(BaseModel):
    crop: str = Field(..., json_schema_extra={"example": "tomato"}, description="Intended crop to sow")
    district: str = Field(..., json_schema_extra={"example": "Idukki"}, description="Farmer's district or region in Kerala")
    lat: Optional[float] = Field(None, json_schema_extra={"example": 9.8494}, description="Optional latitude for live weather")
    lon: Optional[float] = Field(None, json_schema_extra={"example": 76.9814}, description="Optional longitude for live weather")


class ForecastSummary(BaseModel):
    avg_temp_c: float
    min_temp_c: float
    max_temp_c: float
    total_rainfall_next_7d_mm: float
    rain_probability_pct: int
    humidity_avg_pct: float
    weather_condition: str
    is_live_data: bool


class SowingWindowDetail(BaseModel):
    season_name: str
    recommended_start: str
    recommended_end: str
    is_currently_in_window: bool
    sowing_tips: Optional[str] = None


class WeatherAdvisoryResponse(BaseModel):
    success: bool = True
    crop: str
    district: str
    is_safe_to_sow: bool
    safety_status: str # "SAFE_TO_SOW", "CAUTION", "NOT_RECOMMENDED"
    recommended_window: SowingWindowDetail
    forecast_summary: ForecastSummary
    risk_factors: List[str]
    advisory_notes: str


class ChatMessage(BaseModel):
    role: str # "user" or "assistant"
    content: str


class AdvisoryChatContext(BaseModel):
    district: Optional[str] = "Idukki"
    crop: Optional[str] = "tomato"
    soil_type: Optional[str] = "Hill soil / Laterite loam"
    suitability_score: Optional[float] = 85.0
    suitability_category: Optional[str] = "High"
    is_safe_to_sow: Optional[bool] = True
    seed_price_range: Optional[str] = "₹350 - ₹450 / 100g"
    weather_forecast: Optional[str] = "Moderate rainfall (35mm over 7 days), 22-26°C"
    extra_details: Optional[Dict[str, Any]] = None


class AdvisoryChatRequest(BaseModel):
    farmer_name: Optional[str] = "Farmer"
    question: str = Field(..., json_schema_extra={"example": "Is it a good time to plant tomatoes here in Idukki?"})
    conversation_history: Optional[List[ChatMessage]] = []
    context: Optional[AdvisoryChatContext] = None


class AdvisoryChatResponse(BaseModel):
    success: bool = True
    farmer_name: str
    reply: str
    actionable_tips: List[str]
    suggested_followups: List[str]
