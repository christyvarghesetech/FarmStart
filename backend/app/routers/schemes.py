from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional, List, Dict, Any
from app.database import get_db
from app.models import GovernmentScheme, Crop
from app.data.seed_data import KERALA_DISTRICTS

router = APIRouter(tags=["Schemes & Reference Data"])


@router.get(
    "/government-schemes",
    summary="Government agricultural subsidy and scheme eligibility alerts"
)
def get_schemes(
    crop: Optional[str] = Query(None, description="Filter by crop (e.g. tomato, rice)"),
    db: Session = Depends(get_db)
):
    """
    Returns government schemes, subsidies, and insurance options (e.g. Subhiksha Keralam,
    PMFBY, MIDH) relevant to the farmer's crop selection.
    """
    schemes = db.query(GovernmentScheme).all()

    results = []
    crop_clean = crop.strip().lower().replace(" ", "_") if crop else None

    for s in schemes:
        targets = s.target_crops or []
        if not crop_clean or "all" in targets or crop_clean in targets or "vegetables" in targets:
            results.append({
                "id": s.id,
                "title": s.title,
                "department": s.department,
                "target_crops": s.target_crops,
                "benefits": s.benefits,
                "eligibility": s.eligibility,
                "application_mode": s.application_mode,
                "documentation": s.documentation
            })

    return {
        "success": True,
        "count": len(results),
        "schemes": results
    }


@router.get(
    "/districts",
    summary="List Kerala agricultural districts and soil health defaults"
)
def get_districts():
    """
    Returns all 14 Kerala districts with default soil types, climate zones,
    and NPK baseline ranges for frontend selection.
    """
    items = []
    for d_name, d_data in KERALA_DISTRICTS.items():
        items.append({
            "district": d_name,
            "primary_soil": d_data["primary_soil"],
            "soil_types": d_data["soil_types"],
            "climate_zone": d_data["climate_zone"],
            "default_npk": d_data["default_npk"],
            "lat": d_data["lat"],
            "lon": d_data["lon"]
        })
    return {"success": True, "count": len(items), "districts": items}


@router.get(
    "/crops",
    summary="List supported crops and categories"
)
def get_crops(db: Session = Depends(get_db)):
    """
    Returns crops catalog for frontend dropdowns and quick selector.
    """
    crops = db.query(Crop).all()
    return {
        "success": True,
        "count": len(crops),
        "crops": [
            {
                "id": c.id,
                "name": c.name,
                "scientific_name": c.scientific_name,
                "category": c.category,
                "sowing_season": c.sowing_season,
                "promising_districts": c.promising_districts,
                "recommended_varieties": c.recommended_varieties
            }
            for c in crops
        ]
    }
