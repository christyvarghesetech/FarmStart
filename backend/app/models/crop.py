from sqlalchemy import Column, Integer, String, Float, Text, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.database import Base

class Crop(Base):
    __tablename__ = "crops"

    id = Column(String(50), primary_key=True, index=True) # e.g. "tomato", "rice"
    name = Column(String(100), nullable=False, index=True)
    scientific_name = Column(String(100), nullable=True)
    category = Column(String(50), nullable=False) # "Vegetables", "Spices", etc.
    ideal_soil_types = Column(JSON, nullable=False) # list of soil strings
    ideal_ph_range = Column(JSON, nullable=True) # [min, max]
    ideal_temp_c = Column(JSON, nullable=True) # [min, max]
    ideal_monthly_rainfall_mm = Column(JSON, nullable=True) # [min, max]
    sowing_season = Column(String(200), nullable=False)
    promising_districts = Column(JSON, nullable=True)
    recommended_varieties = Column(JSON, nullable=True)
    maturity_days = Column(String(50), nullable=True)
    notes = Column(Text, nullable=True)

    seed_prices = relationship("SeedPrice", back_populates="crop")
    sowing_windows = relationship("SowingWindow", back_populates="crop")


class SoilRegion(Base):
    __tablename__ = "soil_regions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    district = Column(String(100), nullable=False, index=True)
    soil_type = Column(String(100), nullable=False)
    climate_zone = Column(String(100), nullable=True)
    avg_annual_rainfall_mm = Column(Float, nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    default_n = Column(Float, nullable=True)
    default_p = Column(Float, nullable=True)
    default_k = Column(Float, nullable=True)
    default_ph = Column(Float, nullable=True)


class SeedPrice(Base):
    __tablename__ = "seed_prices"

    id = Column(Integer, primary_key=True, autoincrement=True)
    crop_id = Column(String(50), ForeignKey("crops.id"), nullable=False, index=True)
    crop_name = Column(String(100), nullable=False)
    region = Column(String(100), nullable=False, index=True) # District or State
    min_price = Column(Float, nullable=False)
    max_price = Column(Float, nullable=False)
    modal_price = Column(Float, nullable=False)
    unit = Column(String(100), nullable=False) # e.g. "per 100g", "per kg"
    source = Column(String(200), nullable=False) # e.g. "KSSDA / e-NAM"
    varieties = Column(JSON, nullable=True)

    crop = relationship("Crop", back_populates="seed_prices")


class SowingWindow(Base):
    __tablename__ = "sowing_windows"

    id = Column(Integer, primary_key=True, autoincrement=True)
    crop_id = Column(String(50), ForeignKey("crops.id"), nullable=False, index=True)
    region = Column(String(100), nullable=False, index=True)
    season_name = Column(String(150), nullable=True)
    recommended_start = Column(String(50), nullable=False) # MM-DD or descriptive
    recommended_end = Column(String(50), nullable=False)
    safe_rainfall_min_mm = Column(Float, nullable=True)
    safe_rainfall_max_mm = Column(Float, nullable=True)
    safe_temp_min_c = Column(Float, nullable=True)
    safe_temp_max_c = Column(Float, nullable=True)
    sowing_tips = Column(Text, nullable=True)

    crop = relationship("Crop", back_populates="sowing_windows")


class GovernmentScheme(Base):
    __tablename__ = "government_schemes"

    id = Column(String(100), primary_key=True)
    title = Column(String(255), nullable=False)
    department = Column(String(255), nullable=False)
    target_crops = Column(JSON, nullable=False) # ["tomato", "all", etc.]
    eligibility = Column(Text, nullable=False)
    benefits = Column(Text, nullable=False)
    application_mode = Column(String(255), nullable=True)
    documentation = Column(Text, nullable=True)
