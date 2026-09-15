"""
Initialize and Seed the FarmStart Database
Creates tables and seeds initial Kerala agronomic datasets.
"""

import os
import sys

# Ensure backend root is on sys.path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from app.database import Base, engine, SessionLocal
from app.models import Crop, SoilRegion, SeedPrice, SowingWindow, GovernmentScheme, Farmer
from app.data.seed_data import KERALA_DISTRICTS, CROPS_CATALOG, SEED_PRICES, SOWING_CALENDARS, GOVERNMENT_SCHEMES


def init_database():
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        # 1. Seed Soil Regions / Districts
        if db.query(SoilRegion).count() == 0:
            print("Seeding Kerala soil regions & districts...")
            for district_name, info in KERALA_DISTRICTS.items():
                for s_type in info["soil_types"]:
                    region_record = SoilRegion(
                        district=district_name,
                        soil_type=s_type,
                        climate_zone=info["climate_zone"],
                        avg_annual_rainfall_mm=info["avg_annual_rainfall_mm"],
                        latitude=info["lat"],
                        longitude=info["lon"],
                        default_n=info["default_npk"]["N"],
                        default_p=info["default_npk"]["P"],
                        default_k=info["default_npk"]["K"],
                        default_ph=info["default_npk"]["ph"]
                    )
                    db.add(region_record)
            db.commit()

        # 2. Seed Crops
        if db.query(Crop).count() == 0:
            print("Seeding crops catalog...")
            for c in CROPS_CATALOG:
                crop_record = Crop(
                    id=c["id"],
                    name=c["name"],
                    scientific_name=c.get("scientific_name"),
                    category=c["category"],
                    ideal_soil_types=c["ideal_soil_types"],
                    ideal_ph_range=c.get("ideal_ph_range"),
                    ideal_temp_c=c.get("ideal_temp_c"),
                    ideal_monthly_rainfall_mm=c.get("ideal_monthly_rainfall_mm"),
                    sowing_season=c["sowing_season"],
                    promising_districts=c.get("promising_districts"),
                    recommended_varieties=c.get("recommended_varieties"),
                    maturity_days=c.get("maturity_days"),
                    notes=c.get("notes")
                )
                db.add(crop_record)
            db.commit()

        # 3. Seed Seed Prices
        if db.query(SeedPrice).count() == 0:
            print("Seeding seed price benchmarks...")
            for sp in SEED_PRICES:
                price_record = SeedPrice(
                    crop_id=sp["crop_id"],
                    crop_name=sp["crop_name"],
                    region=sp["region"],
                    min_price=sp["min_price"],
                    max_price=sp["max_price"],
                    modal_price=sp["modal_price"],
                    unit=sp["unit"],
                    source=sp["source"],
                    varieties=sp.get("varieties", [])
                )
                db.add(price_record)
            db.commit()

        # 4. Seed Sowing Calendars
        if db.query(SowingWindow).count() == 0:
            print("Seeding sowing windows...")
            for sw in SOWING_CALENDARS:
                sw_record = SowingWindow(
                    crop_id=sw["crop_id"],
                    region=sw["region"],
                    season_name=sw.get("season_name"),
                    recommended_start=sw["start_date"],
                    recommended_end=sw["end_date"],
                    safe_rainfall_min_mm=sw.get("safe_rainfall_min_mm"),
                    safe_rainfall_max_mm=sw.get("safe_rainfall_max_mm"),
                    safe_temp_min_c=sw.get("safe_temp_min_c"),
                    safe_temp_max_c=sw.get("safe_temp_max_c"),
                    sowing_tips=sw.get("sowing_tips")
                )
                db.add(sw_record)
            db.commit()

        # 5. Seed Government Schemes
        if db.query(GovernmentScheme).count() == 0:
            print("Seeding government schemes...")
            for gs in GOVERNMENT_SCHEMES:
                scheme_record = GovernmentScheme(
                    id=gs["id"],
                    title=gs["title"],
                    department=gs["department"],
                    target_crops=gs["target_crops"],
                    eligibility=gs["eligibility"],
                    benefits=gs["benefits"],
                    application_mode=gs.get("application_mode"),
                    documentation=gs.get("documentation")
                )
                db.add(scheme_record)
            db.commit()

        # 6. Seed Demo Farmer (Anil in Idukki)
        if db.query(Farmer).count() == 0:
            print("Seeding demo farmer Anil (Idukki)...")
            demo_farmer = Farmer(
                name="Anil",
                location="Idukki",
                preferred_language="en",
                phone="+919876543210"
            )
            db.add(demo_farmer)
            db.commit()

        print("Database initialization & seeding complete!")

    except Exception as e:
        db.rollback()
        print(f"Error seeding database: {e}")
        raise e
    finally:
        db.close()


if __name__ == "__main__":
    init_database()
