from typing import List, Optional, Dict, Any
from pydantic import BaseModel


class VarietyBenchmark(BaseModel):
    variety: str
    price: float
    type: Optional[str] = "Certified"


class SeedPriceDetail(BaseModel):
    min_price: float
    max_price: float
    modal_price: float
    fair_price_range: str
    unit: str
    source: str
    varieties: List[Dict[str, Any]] = []


class SeedPriceResponse(BaseModel):
    success: bool = True
    crop: str
    region: str
    min_price: float
    max_price: float
    modal_price: float
    fair_price_range: str
    unit: str
    source: str
    varieties: List[Dict[str, Any]] = []
    # Live market rate enhancement
    is_live: Optional[bool] = False
    primary_mandi: Optional[str] = None
    produce_market_price: Optional[Dict[str, Any]] = None
    price_summary_note: Optional[str] = None


class LiveMarketPriceResponse(BaseModel):
    success: bool = True
    crop: str
    region: str
    is_live: bool
    primary_mandi: str
    last_updated: str
    seed_input_price: SeedPriceDetail
    produce_market_price: Dict[str, Any]
    price_summary_note: str


class CropFitItem(BaseModel):
    crop_id: str
    name: str
    scientific_name: Optional[str] = None
    category: str
    suitability_rating: str # "Highly Recommended", "Moderately Recommended", "Suitable with Soil Care"
    ideal_soil_types: List[str]
    sowing_season: str
    recommended_varieties: List[str]
    maturity_days: Optional[str] = None
    notes: Optional[str] = None


class CropFitResponse(BaseModel):
    success: bool = True
    district: str
    soil_type: str
    climate_zone: Optional[str] = None
    suitable_crops: List[CropFitItem]
