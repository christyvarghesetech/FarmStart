from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class SuitabilityRequest(BaseModel):
    crop: str = Field(..., json_schema_extra={"example": "tomato"}, description="Target crop (e.g. tomato, rice, banana, cardamom)")
    district: str = Field(..., json_schema_extra={"example": "Idukki"}, description="District in Kerala")
    soil_type: Optional[str] = Field(None, json_schema_extra={"example": "Hill soil"}, description="Soil type; auto-detected if empty")
    nitrogen: Optional[float] = Field(None, json_schema_extra={"example": 75.0}, description="Nitrogen content (kg/ha or index)")
    phosphorus: Optional[float] = Field(None, json_schema_extra={"example": 42.0}, description="Phosphorus content (kg/ha or index)")
    potassium: Optional[float] = Field(None, json_schema_extra={"example": 58.0}, description="Potassium content (kg/ha or index)")
    ph: Optional[float] = Field(None, json_schema_extra={"example": 6.2}, description="Soil pH value")
    temperature: Optional[float] = Field(None, json_schema_extra={"example": 23.5}, description="Average temperature in Celsius")
    humidity: Optional[float] = Field(None, json_schema_extra={"example": 75.0}, description="Relative humidity %")
    rainfall: Optional[float] = Field(None, json_schema_extra={"example": 160.0}, description="Expected monthly rainfall in mm")


class SuitabilityResponse(BaseModel):
    success: bool = True
    crop: str
    district: str
    soil_type: str
    suitability_category: str # "High", "Medium", "Low"
    suitability_score: float # 0 to 100
    ml_confidence_pct: float
    probabilities: Dict[str, float]
    yield_prediction: str
    limiting_factors: List[str]
    key_recommendations: List[str]
    soil_parameters_used: Dict[str, Any]
