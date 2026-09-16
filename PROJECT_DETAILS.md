# FarmStart: New Farmer Agricultural Copilot (Kerala)
### Comprehensive Project Documentation & Technical Architecture Report
**Event / Track**: Agriculture Track — AI Conclave 2026, Amal Jyothi College of Engineering  
**Target Beneficiaries**: First-time cultivators, youth agrarians, Kudumbashree collectives, and transitioning farmers across Kerala's 14 agro-climatic districts.

---

## 1. Executive Summary

### The Problem
Over **60% of first-time and smallholder farmers in Kerala encounter crop failure or debt during their initial three seasons**. The root causes are systemic:
1. **Uninformed Sowing Timing**: Sowing seeds during sudden heavy rains causes seed wash-off, fungal damping-off, and seedling mortality.
2. **Seed Input Exploitation**: Commercial seed vendors frequently overcharge new growers by 200–400% for uncertified varieties.
3. **Agronomic Jargon Overload**: Scientific recommendations from agricultural universities are dense, technical, and locked in thick PDF manuals.
4. **Post-Harvest Distress Selling**: Without visibility into market trends or storage viability, smallholders dump produce at local gluts for rock-bottom prices.
5. **Preventable Pest & Disease Losses**: Farmers lose 40–60% of crop yields to common pests because they cannot identify early symptoms or spray the wrong chemical pesticides too late.

### The FarmStart Solution
**FarmStart** is an end-to-end, AI-powered agricultural decision-support platform designed to eliminate guesswork from farming. It combines:
* **Real-time meteorological forecasting** (Open-Meteo API) to evaluate safe sowing windows.
* **Scikit-Learn Machine Learning** trained on Kerala Agricultural University (KAU) agronomy rules to score crop suitability (0–100%).
* **Fair seed price benchmarking** (KSSDA & e-NAM) to protect farmers from input price gouging.
* **30-day harvest price prediction & Mandi Heatmap** with an automated economic engine that advises whether to **Sell Fresh** or **Hold in Cold Storage**.
* **KAU Integrated Pest Management (IPM)** with weather-triggered threat alerts and dual-track (**Organic Bio-Remedy vs. Emergency Chemical**) recipes.
* **Conversational AI Copilot** powered by Groq LPUs delivering plain-language answers with 3 clear action steps.
* **Authentic Bilingual Malayalam & English Interface** featuring Google's Noto Sans Malayalam typography.

---

## 2. System Architecture & Tech Stack

```
+-----------------------------------------------------------------------------------+
|                                  CLIENT LAYER                                     |
|  - Responsive HTML5 & Tailwind CSS                                                |
|  - Chart.js (30-Day Price Trend Curves & Confidence Bands)                        |
|  - FontAwesome 6 Icons & Noto Sans Malayalam Typography                           |
|  - LocalStorage Language State (English <-> Malayalam Toggle)                     |
+-----------------------------------------------------------------------------------+
                                         │  HTTP / JSON REST API
                                         ▼
+-----------------------------------------------------------------------------------+
|                                FASTAPI BACKEND (Port 8000)                        |
|  - Uvicorn ASGI Server & CORS Middleware                                          |
|  - SQLAlchemy ORM & SQLite Database (farmstart.db)                                |
|  - Modular Routers: advisory, suitability, prices, schemes, pest_advisory         |
+-----------------------------------------------------------------------------------+
        │                       │                       │                     │
        ▼                       ▼                       ▼                     ▼
+---------------+       +---------------+       +---------------+     +-------------+
|  ML ENGINE    |       | WEATHER ENGINE|       | MANDI PREDICTOR|    | GROQ COPILOT|
| Scikit-Learn  |       | Open-Meteo API|       | 30-Day Trend  |     | LPU Cloud   |
| RandomForest  |       | 7-Day Rain &  |       | Storage ROI   |     | qwen/qwen3.8|
| Classifier    |       | Humidity Feed |       | 6 APMC Mandis |     | Llama-3.3   |
+---------------+       +---------------+       +---------------+     +-------------+
```

### Technology Breakdown

| Component | Technology | Role in System |
| :--- | :--- | :--- |
| **Frontend Framework** | Vanilla HTML5 / ES6 JavaScript | Zero build-step frontend, instant loading, maximum rural browser compatibility |
| **Styling & Design** | Tailwind CSS (CDN) | Modern clean white aesthetic, card layouts, responsive grid, status badges |
| **Data Visualization** | Chart.js 4.x | Smooth 30-day price trajectory curves (Actuals vs. AI Forecast with tooltips) |
| **Typography** | Plus Jakarta Sans & Noto Sans Malayalam | Crisp dual-script rendering for high Malayalam readability |
| **Backend Framework** | FastAPI (Python 3.12) | High-performance async REST API with interactive Swagger docs (`/docs`) |
| **Database** | SQLite + SQLAlchemy ORM | Local persistence for crops, districts, baseline NPK, seed prices, and schemes |
| **Machine Learning** | Scikit-learn (RandomForestClassifier) | Evaluates district soil, NPK, pH, and live weather to predict suitability |
| **LLM Reasoning** | Groq Cloud LPU (`qwen/qwen3.8-27b`) | Low-latency plain-language conversational advisory with prompt injection safety |
| **Live Weather API** | Open-Meteo Meteorological API | Real-time hourly & daily weather data using ECMWF & DWD numerical models |
| **Market Data** | Agmarknet (data.gov.in) & e-NAM / VFPCK | Live mandi trading prices and official KSSDA seed benchmark tariffs |

---

## 3. Core Features Breakdown

### Feature 1: Instant Sowing Feasibility & ML Suitability Calculator
* **What it does**: Takes the farmer's District, Soil Type, and Intended Crop, and instantly evaluates whether it is safe to plant today.
* **How it works**:
  1. Calls Open-Meteo for real-time 7-day rainfall, average temperature, and relative humidity.
  2. Runs the scikit-learn `RandomForestClassifier` against soil NPK, pH, and weather to generate a **Suitability Score (0–100%)** and Category (`High`, `Medium`, `Low`).
  3. Evaluates agronomic rules to output a prominent Sowing Status Badge:
     * `SAFE TO SOW NOW` (Emerald): Weather is within optimal moisture bounds.
     * `PROCEED WITH CAUTION` (Amber): Moderate rainfall or soil drainage precautions needed.
     * `SOWING NOT RECOMMENDED` (Rose): Imminent heavy rainfall will cause seed rotting/washout.
  4. Returns safe planting window dates aligned with Kerala seasonal cycles (*Virippu, Mundakan, Puncha*).

### Feature 2: Harvest Price Predictor & Mandi Heatmap (30-Day Forecasting)
* **What it does**: Displays a continuous 30-day wholesale commodity price curve (15 days of historical actuals + 14 days of forward AI projections) and compares rates across 6 major Kerala APMC wholesale markets.
* **Storage vs. Fresh Sell Economic Engine**:
  * Evaluates crop perishability (*High, Moderate, Low*), daily storage fees (~₹0.03–₹0.25/kg/day), and quality decay.
  * Issues an automated financial decision:
    * `SELL FRESH IMMEDIATELY`: When storage costs and spoilage outweigh price appreciation (e.g. Tomato).
    * `HOLD IN COLD STORAGE / WAREHOUSE`: When projected 14-day price surge yields positive net ROI after storage fees (e.g. Cardamom showing +7.5% net ROI).
    * `SPLIT HARVEST (50% Fresh, 50% Hold)`: Hedging strategy for moderate volatility.
  * Recommends the exact regional storage facility (e.g., *Spices Board Spices Park Puttady*, *KSWC Grain Silo Palakkad*, *VFPCK Packhouse Aluva*).
* **Kerala Mandi Heatmap Grid**:
  * Compares wholesale prices across:
    1. Nedumkandam Mandi / Spices Park Puttady (Idukki)
    2. Vyttila Wholesale Market / Kochi Terminal (Ernakulam)
    3. Vellanikkara / Thrissur Wholesale Market (Thrissur)
    4. Palakkad Regulated Market (Palakkad)
    5. Kalpetta APMC Market (Wayanad)
    6. Anayara World Market (Thiruvananthapuram)
  * Displays transport-adjusted net prices, price difference vs. local district market, and highlights the **Best Net Rate** market.

### Feature 3: Pest & Disease Intelligence & Organic Control (KAU IPM)
* **What it does**: Anticipates pest and fungal outbreaks before damage occurs using live meteorological triggers.
* **Real-Time Weather Risk Alerts**:
  * Cross-references today's real-time atmospheric humidity and temperature against outbreak thresholds.
  * If humidity exceeds 80% and temperatures match fungal spore dispersal ranges $\implies$ dynamically raises an **Active Weather Trigger Alert** banner.
* **Dual-Track Treatment Protocols**:
  * **🌿 Organic Bio-Remedies (Recommended)**: Step-by-step preparation for KAU bio-formulations (*Neem-Garlic soap emulsion, 1% Bordeaux mixture, Trichoderma viride, Beauveria bassiana*).
  * **🧪 Chemical Alternatives**: Exact dosage per liter, Pre-Harvest Intervals (PHI in days), and pollinator/bee protection rules.
  * **Cultural IPM**: Pheromone traps, yellow sticky traps, companion planting, and spacing.
* **Interactive Symptom Filters**: Quick-filter by *All Pests*, *Leaf Symptoms*, *Fruit/Pod Damage*, and *Stem & Wilt Rot*.
* **AI Copilot Link**: One-click button on each card to ask the AI Copilot for personalized home-mixing advice.

### Feature 4: Fair Seed Price Benchmark & Anti-Exploitation Tariff
* **What it does**: Protects new growers from overpaying for seed inputs.
* **Data Sources**: Official Kerala State Seed Development Authority (KSSDA) tariffs and e-NAM reference rates.
* **Output**: Fair price range (e.g., *₹350 - ₹450 per 100g certified seeds*), modal baseline, certified KAU varieties, and source agency.

### Feature 5: Curated Regional Crop Catalog
* **What it does**: Displays beginner-resilient crops curated for Kerala's agro-climatic conditions.
* **Features**:
  * Authentic crop photographs (`images/crops/`).
  * Ideal soil types, maturity timelines, KAU approved varieties (*Jyothi, Uma, Nendran, Appangala-1, Panniyur-1*).
  * Category tabs: *Vegetables, Spices, Cereals, Fruits, Tubers*.
  * One-click "Check Sowing Feasibility" button that pre-loads the crop into the feasibility tool.

### Feature 6: Groq AI Agricultural Copilot Chat
* **What it does**: Conversational farming assistant accessible 24/7.
* **Capabilities**:
  * Real-time reasoning using Groq LPUs (`qwen/qwen3.8-27b` / `llama-3.3-70b`).
  * System prompt grounded in KAU guidelines, soil chemistry, and weather data.
  * Prompt injection prevention and agricultural domain guardrails.
  * Every response formatted with **3 actionable takeaways** and suggested follow-up chips.
  * Dynamic Farmer Persona: Allows entering custom farmer names (e.g., Anil, Suresh, Thomas).

### Feature 7: Government Subsidies & Schemes Portal
* **What it does**: Connects farmers directly to state and central government grant schemes.
* **Integrated Schemes**:
  1. *Subhiksha Keralam Integrated Food Security Mission* (₹20,000–₹30,000/ha for fallow land farming).
  2. *PM-KISAN* (₹6,000/year direct benefit transfer).
  3. *PMFBY* (Restructured Weather Based Crop Insurance at 1.5%–2% premium).
  4. *MIDH / State Horticulture Mission* (Up to 50% capital subsidy for drip irrigation & polyhouses).
  5. *KSSDA Seed Distribution Subsidy* (25%–50% discount on certified seeds).
* **Direct Links**: Direct action button to the Kerala Agriculture Information Management System ([AIMS Portal `aims.kerala.gov.in`](https://aims.kerala.gov.in)).

### Feature 8: Complete Bilingual Malayalam & English Typography
* **What it does**: Instant one-click toggle between English and authentic Malayalam script.
* **Key Implementations**:
  * Google's **Noto Sans Malayalam** font integrated with custom line-height and weight balance.
  * Persistent language choice saved in `localStorage`.
  * Dynamic translations for navigation, hero banners, advisory metrics, crop catalog, mandi heatmap, pest remedies, and modal windows.
  * When Malayalam is active, the AI Copilot automatically responds in natural Malayalam (*ലളിതമായ മലയാളത്തിൽ മറുപടി നൽകുന്നു*).

---

## 4. Complete Datasets Used & Authoritative Sources

| # | Dataset Name | Storage / Type | Authoritative Source |
| :--- | :--- | :--- | :--- |
| 1 | **Crop Agronomy & Scientific Varieties** | SQLite / Seed Data | **Kerala Agricultural University (KAU)** — *Package of Practices: Crops* |
| 2 | **Agro-Climatic Zones & Soil Health Cards** | SQLite / Seed Data | **Soil Health Card Scheme (GoI & GoK)** / Kerala State Land Use Board |
| 3 | **ML Crop Suitability Dataset (1,600+ samples)**| Scikit-learn Trained Model | Synthesized from KAU agronomic bounds & ICAR tolerance matrices |
| 4 | **Seed Price Benchmarks & Mandi Baselines** | SQLite / Seed Data | **KSSDA**, **Agmarknet / e-NAM**, **VFPCK** Price Bulletins |
| 5 | **7-Day Meteorological Forecasts** | Real-Time Live API | **Open-Meteo API** (ECMWF & DWD meteorological models) |
| 6 | **Pest & Disease Intelligence (13+ Profiles)** | Structured Python Dataset | **KAU Integrated Pest Management (IPM)** & ICAR-IISR Handbooks |
| 7 | **Wholesale Mandis Network (6 APMC Mandis)** | Python Market Service | **e-NAM**, Kerala State Agricultural Marketing Board, Spices Board |
| 8 | **Government Grants & Subsidies** | SQLite / Seed Data | **AIMS Portal (Govt. of Kerala)**, PM-KISAN, PMFBY Guidelines |

---

## 5. API Reference (Backend Endpoints)

FastAPI provides automated interactive OpenAPI Swagger documentation accessible at `http://127.0.0.1:8000/docs`.

### Primary Endpoints:

1. `GET /`
   * Health status, project version, active track, and endpoints catalog.
2. `POST /full-advisory`
   * Combined one-shot endpoint executing weather check, ML suitability scoring, seed benchmark lookup, and initial AI advisory.
3. `POST /weather-advisory`
   * Returns 7-day live weather metrics and safe sowing feasibility for a district.
4. `POST /suitability-score`
   * Runs the trained Random Forest classifier against NPK, pH, temperature, humidity, and rainfall.
5. `GET /harvest-price-predictor`
   * Returns 30-day price time series, 6-mandi comparative heatmap, and cold storage ROI verdict.
6. `GET /pest-advisory`
   * Returns crop-specific pests, real-time meteorological trigger alerts, and dual-track (organic vs chemical) remedies.
7. `GET /seed-price-check`
   * Returns fair seed purchase price range, modal rates, and verified KAU varieties.
8. `GET /live-market-price`
   * Returns daily wholesale mandi auction rates.
9. `GET /crop-fit`
   * Returns curated crops ranked by suitability for a specific Kerala district.
10. `GET /government-schemes`
    * Returns eligible state and central subsidies filtered by crop category.
11. `POST /advisory-chat`
    * Streaming conversational AI copilot with session history and prompt injection filtering.
12. `GET /districts`
    * Lists all 14 Kerala districts with geographic coordinates, soil types, and default NPK profiles.

---

## 6. How to Run the Project Locally

### Prerequisites
* Python 3.10+ (Python 3.12 recommended)
* Google Chrome, Microsoft Edge, or Firefox

### One-Click Launch
Double-click `start.bat` located in the project root:
```batch
start.bat
```
This launcher checks Python, automatically installs missing packages from `backend/requirements.txt`, boots the FastAPI ASGI server on port 8000, and opens the application in your default browser.

### Manual Launch via Terminal
```powershell
# From the project root directory
cd c:\Users\ADMIN\OneDrive\Desktop\FarmStart
python run_app.py
```
* **Application Web UI**: `http://127.0.0.1:8000/app/`
* **Interactive API Docs**: `http://127.0.0.1:8000/docs`
* **Raw Health API**: `http://127.0.0.1:8000/`

---

## 7. Project Directory Structure

```
FarmStart/
├── start.bat                    # One-click Windows launcher
├── run_app.py                   # Master runner (installs requirements & boots server)
├── PROJECT_DETAILS.md           # This comprehensive documentation file
├── frontend/
│   ├── index.html               # Main responsive web application (bilingual UI)
│   └── images/
│       └── crops/               # Authentic high-resolution crop photography
│           ├── tomato.jpg
│           ├── rice.jpg
│           ├── banana.jpg
│           ├── cardamom.jpg
│           ├── black_pepper.jpg
│           ├── ginger.jpg
│           ├── tapioca.jpg
│           ├── okra.jpg
│           └── chilli.jpg
└── backend/
    ├── requirements.txt         # Python dependencies (FastAPI, scikit-learn, groq, etc.)
    ├── .env                     # Environment variables (GROQ_API_KEY, DATA_GOV_IN_API_KEY)
    ├── farmstart.db             # Local SQLite database
    ├── scripts/
    │   ├── init_db.py           # Database seeder (crops, districts, seed prices, schemes)
    │   └── train_suitability_model.py # Random Forest ML trainer (KAU agronomic rules)
    └── app/
        ├── main.py              # FastAPI application setup & static mount
        ├── config.py            # Pydantic environment configuration
        ├── database.py          # SQLAlchemy session engine
        ├── models/              # Database ORM models (Crop, SeedPrice, Scheme, etc.)
        ├── schemas/             # Pydantic request & response validation schemas
        ├── data/
        │   ├── seed_data.py     # Base Kerala agricultural datasets
        │   ├── pest_data.py     # KAU Integrated Pest Management (IPM) dataset
        │   └── ml_models/       # Serialized scikit-learn model & encoders (.joblib)
        ├── services/
        │   ├── ml_service.py    # Random Forest inference engine
        │   ├── weather_service.py # Open-Meteo real-time integration
        │   ├── sowing_service.py  # Sowing window feasibility evaluator
        │   ├── price_service.py   # Seed benchmark & mandi pricing logic
        │   ├── mandi_predictor.py # 30-day price trend & cold storage decision engine
        │   ├── pest_service.py    # Real-time weather-linked pest risk calculator
        │   └── llm_service.py     # Groq LPU conversational advisory engine
        └── routers/
            ├── advisory.py      # Sowing feasibility & copilot chat endpoints
            ├── suitability.py   # ML scoring endpoints
            ├── prices.py        # Seed prices, crop fit, & harvest predictor endpoints
            ├── schemes.py       # Government subsidies & districts endpoints
            └── pest_advisory.py # Pest & disease intelligence endpoints
```

---

## 8. Presentation & Pitch Highlights (For Judges / Evaluators)

1. **Grounded in Authentic Regional Science**: Built specifically for Kerala’s unique humid tropical and highland agro-climatic zones using **Kerala Agricultural University** Package of Practices.
2. **Real-Time Integration**: Not a toy mock-up; actively calls **Open-Meteo** live weather and dynamically recalculates fungal infection risks and sowing windows on the fly.
3. **End-to-End Decision Lifecycle**: Guides the farmer across the complete crop cycle:
   * **Before Planting**: Sowing feasibility, safe window, and ML suitability.
   * **During Purchase**: Fair seed price benchmark (anti-gouging).
   * **During Cultivation**: Weather-driven pest alerts and organic bio-remedies.
   * **At Harvest**: 30-day price forecasting, mandi heatmap, and cold storage ROI verdict.
4. **Inclusive Vernacular Accessibility**: Features native **Malayalam script typography** so smallholders and Kudumbashree farmers can use the platform without language barriers.
