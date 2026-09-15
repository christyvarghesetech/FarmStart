import os
from pathlib import Path
from dotenv import load_dotenv

# Load from .env file if available
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

class Settings:
    PROJECT_NAME: str = "FarmStart Backend"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "New Farmer Copilot API - AI Conclave 2026 Hackathon"

    DATABASE_URL: str = os.getenv("DATABASE_URL", f"sqlite:///{BASE_DIR}/farmstart.db")
    
    # LLM Settings
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    GROQ_MODEL: str = os.getenv("GROQ_MODEL", "qwen/qwen3.8-27b")
    
    # Weather Settings
    OPENWEATHER_API_KEY: str = os.getenv("OPENWEATHER_API_KEY", "")
    DEFAULT_STATE: str = os.getenv("DEFAULT_STATE", "Kerala")

    # Live Market / Agmarknet Settings
    DATA_GOV_IN_API_KEY: str = os.getenv("DATA_GOV_IN_API_KEY", "")

settings = Settings()
