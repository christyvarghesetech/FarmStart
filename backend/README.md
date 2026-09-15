# FarmStart Backend (New Farmer Copilot)

**AI Conclave 2026 — Agriculture Track**  
*Amal Jyothi College of Engineering*  
**Hackathon Date**: 16 September 2026

FarmStart is an AI-powered agricultural decision-support copilot designed to empower first-time and new farmers in Kerala. It combines live meteorological forecasting, scikit-learn machine learning crop suitability scoring, transparent seed price benchmarks, and Groq-accelerated conversational AI.

---

## Features & Endpoints

| Endpoint | Method | Description |
| :--- | :--- | :--- |
| `POST /weather-advisory` | POST | Rule-based sowing calendar and upcoming 7-day weather safety window |
| `POST /suitability-score`| POST | ML-predicted suitability/yield category (`High`, `Medium`, `Low`) and limiting factors |
| `POST /advisory-chat`    | POST | Conversational LLM copilot for farmer Q&A using Groq (Llama 3.3 70B) |
| `GET /seed-price-check`  | GET  | Fair seed price range and verified KSSDA/e-NAM benchmark rates + live mandi summary |
| `GET /live-market-price` | GET  | Live daily APMC Mandi wholesale commodity auction rate + seed input benchmark |
| `GET /crop-fit`          | GET  | Suggests crops, varieties, and sowing calendars based on soil type & district |
| `GET /government-schemes`| GET  | Financial subsidy and scheme eligibility alerts (Subhiksha Keralam, PM-KISAN, PMFBY) |
| `POST /full-advisory`    | POST | Unified endpoint returning weather, ML suitability, price, and chat in one call |
| `GET /districts`         | GET  | List of all 14 Kerala districts with soil and agro-climatic profiles |
| `GET /crops`             | GET  | List of all supported crops |

---

## Quickstart

### 1. Environment Setup
The backend uses Python 3.10+ (tested on Python 3.12).

Activate your virtual environment:
```powershell
& "c:\Users\ADMIN\OneDrive\Desktop\ml model\venv\Scripts\Activate.ps1"
```

Install dependencies if needed:
```bash
pip install -r requirements.txt
```

### 2. Initialize Database and Seed Curated Data
```bash
python scripts/init_db.py
```
*(Creates `farmstart.db` SQLite database pre-populated with Kerala districts, soil health card parameters, KAU crop packages, KSSDA seed prices, and government schemes)*

### 3. (Optional) Re-train ML Suitability Model
```bash
python scripts/train_suitability_model.py
```
*(Trains and exports the Random Forest classifier to `app/data/ml_models/suitability_model.pkl`)*

### 4. Run the API Server
```bash
python run_backend.py
```
Or with Uvicorn directly:
```bash
uvicorn app.main:app --reload --port 8000
```

Interactive Swagger UI documentation is available at:  
👉 **http://127.0.0.1:8000/docs**

---

## Testing

Run the automated test suite with pytest:
```bash
pytest tests/test_api.py -v
```

All 8 test suites validate the core MVP requirements and the PRD demo narrative (Anil in Idukki planting tomatoes).
