# FarmStart - New Farmer Copilot

> **AI Conclave 2026** | Amal Jyothi College of Engineering  
> **Track:** Agriculture  
> **Tagline:** Empowering first-time and transitioning farmers with honest data, machine learning crop matchmaking, and jargon-free conversational AI.

[![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688.svg?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Scikit-Learn](https://img.shields.io/badge/ML-Scikit--Learn-F7931E.svg?logo=scikit-learn&logoColor=white)](https://scikit-learn.org)
[![Groq](https://img.shields.io/badge/LLM-Groq%20LPU%20(Qwen%2027B)-F55036.svg)](https://groq.com)
[![Open-Meteo](https://img.shields.io/badge/Weather-Open--Meteo%20Live-4A90E2.svg)](https://open-meteo.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## The Problem
First-time cultivators face high failure rates due to:
1. **Misleading local advice & vendor price gouging**: Farmers often pay 2x–4x retail markups for uncertified seeds.
2. **Climate & timing volatility**: Planting immediately before heavy monsoon downpours rots seeds and causes damping-off wilt.
3. **Information asymmetry**: University extension documents and soil health cards are filled with dense scientific jargon inaccessible to beginners.

## The Solution
**FarmStart** bridges this gap through a 3-tier intelligent decision engine:
- **ML Biological Suitability**: Scikit-Learn `RandomForestClassifier` trained on 10 biological, soil, and climate features to predict suitability (0-100%) and identify limiting factors.
- **Real-Time Meteorology**: Live 7-day weather forecasting via Open-Meteo cross-referenced with Kerala Agricultural University (KAU) sowing calendars to issue actionable `SAFE`, `CAUTION`, or `UNSAFE` alerts.
- **Fair Seed & Mandi Benchmarks**: Transparent pricing benchmarks from KSSDA (Kerala State Seed Development Authority) and Agmarknet live mandi rates.
- **Conversational AI Copilot**: High-speed conversational LLM (`qwen/qwen3.8-27b` on Groq LPU) that synthesizes all technical data into plain-language advice with 3 specific field action steps.

---

## Repository Structure

```
FarmStart/
  ├── backend/
  │    ├── app/
  │    │    ├── routers/          # API Route controllers (Advisory, Suitability, Prices, Schemes)
  │    │    ├── services/         # ML scoring, weather, sowing calendar, Groq LLM copilot
  │    │    ├── models/           # SQLAlchemy DB models (Crops, SowingWindows, Prices, Soils)
  │    │    ├── schemas/          # Pydantic validation schemas
  │    │    ├── data/             # Seed data and serialized scikit-learn models (.pkl)
  │    │    ├── config.py         # App configuration & settings
  │    │    ├── database.py       # SQLite engine & session
  │    │    └── main.py           # FastAPI entry point & static frontend mounting
  │    ├── tests/                 # Automated pytest test suites
  │    ├── farmstart.db           # Seeded SQLite database
  │    ├── requirements.txt       # Python dependencies
  │    ├── run_backend.py         # Backend runner
  │    └── .env.example           # Environment template
  ├── frontend/
  │    ├── images/crops/          # Verified high-resolution botanical crop images
  │    ├── index.html             # Responsive FarmStart web application
  │    └── code.html              # Reference mockup
  ├── run_app.py                  # Single-command unified project runner
  ├── .gitignore                  # Git ignore rules (protects API keys & cache)
  └── README.md                   # Project documentation
```

---

## Quickstart & Installation

### Prerequisites
- Python 3.10+ installed
- Git

### 1. Clone the Repository
```bash
git clone https://github.com/<your-username>/FarmStart.git
cd FarmStart
```

### 2. Install Backend Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### 3. Configure Environment Variables
Copy the example configuration:
```bash
cp .env.example .env
```
Edit `.env` to insert your free Groq API key:
```env
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=qwen/qwen3.8-27b
```
*(Get a free key at [console.groq.com](https://console.groq.com))*

### 4. Run the Application
From the repository root:
```bash
python run_app.py
```

- **Web Application**: Visit `http://127.0.0.1:8000/app/`
- **Swagger Interactive API Documentation**: Visit `http://127.0.0.1:8000/docs`

---

## API Endpoints Reference

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/` | API Health Check and system metadata |
| `GET` | `/districts` | List 14 Kerala agro-climatic districts & soils |
| `GET` | `/crop-fit` | Regional crop-soil fit checker with KAU varieties |
| `POST` | `/weather-advisory` | 7-day weather forecasting and sowing window safety |
| `POST` | `/suitability-score` | Scikit-learn ML biological suitability scoring |
| `GET` | `/seed-price-check` | Fair seed price benchmarks from KSSDA |
| `GET` | `/live-market-price` | Agmarknet APMC mandi prices |
| `GET` | `/government-schemes` | Eligible Kerala subsidies (Subhiksha Keralam, PM-KISAN) |
| `POST` | `/advisory-chat` | Natural language LLM agronomy copilot |
| `POST` | `/full-advisory` | Composite end-to-end all-in-one advisory payload |

---

## Testing

Run the automated test suite:
```bash
cd backend
pytest tests/ -v
```

---

## Team & Attribution
Built for **AI Conclave 2026** at Amal Jyothi College of Engineering.
