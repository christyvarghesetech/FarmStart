# -*- coding: utf-8 -*-
from fastapi import APIRouter, Query
from typing import Optional
from app.services.pest_service import evaluate_pest_advisory

router = APIRouter(tags=["Pest & Disease Advisory"])


@router.get(
    "/pest-advisory",
    summary="Crop-specific pest and disease alerts, weather risk, and KAU remedies"
)
async def get_pest_advisory(
    crop: str = Query("tomato", description="Crop name (e.g. tomato, rice, cardamom, banana, ginger)"),
    district: Optional[str] = Query("Idukki", description="District in Kerala")
):
    """
    Returns active pest & fungal disease alerts cross-referenced with live meteorology,
    visual symptoms, and dual-track (Organic Bio-remedy vs Chemical) treatment protocols.
    """
    return await evaluate_pest_advisory(crop=crop, district=district)
