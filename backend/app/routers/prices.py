from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
from app.database import get_db
from app.models import SeedPrice, Crop, SoilRegion
from app.schemas.prices import SeedPriceResponse, CropFitResponse, CropFitItem, LiveMarketPriceResponse
from app.services.price_service import get_comprehensive_price_data
from app.data.seed_data import KERALA_DISTRICTS

router = APIRouter(tags=["Seed Prices & Crop Fit"])


@router.get(
    "/seed-price-check",
    response_model=SeedPriceResponse,
    summary="Seed price transparency benchmark lookup"
)
async def get_seed_price(
    crop: str = Query(..., description="Crop name or ID", examples=["tomato"]),
    region: Optional[str] = Query("Idukki", description="District or Region", examples=["Idukki"]),
    db: Session = Depends(get_db)
):
    """
    Returns benchmark fair price range, modal price, certified varieties,
    and verification source (KSSDA / e-NAM) plus latest wholesale mandi trading rates.
    """
    data = await get_comprehensive_price_data(crop=crop, region=region, db=db)
    seed = data["seed_input_price"]

    return {
        "crop": data["crop"],
        "region": data["region"],
        "min_price": seed["min_price"],
        "max_price": seed["max_price"],
        "modal_price": seed["modal_price"],
        "fair_price_range": seed["fair_price_range"],
        "unit": seed["unit"],
        "source": seed["source"],
        "varieties": seed["varieties"],
        "is_live": data["is_live"],
        "primary_mandi": data["primary_mandi"],
        "produce_market_price": data["produce_market_price"],
        "price_summary_note": data["price_summary_note"]
    }


@router.get(
    "/live-market-price",
    response_model=LiveMarketPriceResponse,
    summary="Live daily APMC Mandi commodity & seed intelligence"
)
async def get_live_market_price(
    crop: str = Query(..., description="Crop name (e.g. tomato, rice, banana)", examples=["tomato"]),
    region: Optional[str] = Query("Idukki", description="District or Region in Kerala", examples=["Idukki"]),
    db: Session = Depends(get_db)
):
    """
    Fetches real-time APMC mandi wholesale auction prices (from Agmarknet live API
    or daily Kerala market index) alongside certified seed purchase benchmarks.
    """
    data = await get_comprehensive_price_data(crop=crop, region=region, db=db)
    return {
        "success": True,
        "crop": data["crop"],
        "region": data["region"],
        "is_live": data["is_live"],
        "primary_mandi": data["primary_mandi"],
        "last_updated": data["last_updated"],
        "seed_input_price": data["seed_input_price"],
        "produce_market_price": data["produce_market_price"],
        "price_summary_note": data["price_summary_note"]
    }


@router.get(
    "/crop-fit",
    response_model=CropFitResponse,
    summary="Crop-soil fit and regional variety checker"
)
def get_crop_fit(
    district: str = Query(..., description="District in Kerala", examples=["Idukki"]),
    soil_type: Optional[str] = Query(None, description="Optional soil type"),
    db: Session = Depends(get_db)
):
    """
    Suggests suitable crops, certified KAU varieties, and sowing seasons
    based on the farmer's district and soil characteristics.
    """
    district_clean = district.strip().title()
    dist_info = KERALA_DISTRICTS.get(district_clean)

    resolved_soil = soil_type
    climate_zone = None

    if dist_info:
        climate_zone = dist_info.get("climate_zone")
        if not resolved_soil:
            resolved_soil = dist_info.get("primary_soil")

    if not resolved_soil:
        region_record = db.query(SoilRegion).filter(SoilRegion.district == district_clean).first()
        if region_record:
            resolved_soil = region_record.soil_type
            climate_zone = region_record.climate_zone

    if not resolved_soil:
        resolved_soil = "Laterite soil"

    # Query all crops from database
    all_crops = db.query(Crop).all()
    fit_items = []

    for c in all_crops:
        is_district_favored = bool(c.promising_districts and district_clean in c.promising_districts)
        soil_matches = any(s.lower() in resolved_soil.lower() for s in (c.ideal_soil_types or []))

        if is_district_favored and soil_matches:
            rating = "Highly Recommended"
        elif is_district_favored or soil_matches:
            rating = "Moderately Recommended"
        else:
            rating = "Suitable with Soil Amendments"

        fit_items.append(
            CropFitItem(
                crop_id=c.id,
                name=c.name,
                scientific_name=c.scientific_name,
                category=c.category,
                suitability_rating=rating,
                ideal_soil_types=c.ideal_soil_types or [],
                sowing_season=c.sowing_season,
                recommended_varieties=c.recommended_varieties or [],
                maturity_days=c.maturity_days,
                notes=c.notes
            )
        )

    # Sort so "Highly Recommended" comes first
    rating_priority = {
        "Highly Recommended": 0,
        "Moderately Recommended": 1,
        "Suitable with Soil Amendments": 2
    }
    fit_items.sort(key=lambda x: rating_priority.get(x.suitability_rating, 3))

    return {
        "district": district_clean,
        "soil_type": resolved_soil,
        "climate_zone": climate_zone,
        "suitable_crops": fit_items
    }
