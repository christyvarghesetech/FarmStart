from fastapi import APIRouter, HTTPException
from app.schemas.suitability import SuitabilityRequest, SuitabilityResponse
from app.services.ml_service import score_crop_suitability

router = APIRouter(tags=["Suitability"])


@router.post(
    "/suitability-score",
    response_model=SuitabilityResponse,
    summary="ML-based crop suitability scoring"
)
def compute_suitability_score(payload: SuitabilityRequest):
    """
    Predicts suitability category ('High', 'Medium', 'Low'), composite score (0-100),
    and yield estimates based on trained scikit-learn model and soil/climate factors.
    """
    try:
        result = score_crop_suitability(
            crop=payload.crop,
            district=payload.district,
            soil_type=payload.soil_type,
            nitrogen=payload.nitrogen,
            phosphorus=payload.phosphorus,
            potassium=payload.potassium,
            ph=payload.ph,
            temperature=payload.temperature,
            humidity=payload.humidity,
            rainfall=payload.rainfall
        )
        return result

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Suitability scoring model error: {str(e)}"
        )
