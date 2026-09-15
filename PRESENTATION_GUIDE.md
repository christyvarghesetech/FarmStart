# FarmStart: New Farmer Copilot
## Complete Presentation & Pitch Deck Reference Guide (Slide-by-Slide)

**Event:** AI Conclave 2026 | Amal Jyothi College of Engineering  
**Track:** Agriculture  
**Repository:** https://github.com/christyvarghesetech/FarmStart  
**Live Demo:** http://127.0.0.1:8000/app/  

---

## Slide 1: Title & Introduction
* **Slide Title:** FarmStart — The AI-Powered New Farmer Copilot
* **Subtitle:** Empowering First-Time Cultivators with Machine Learning, Live Meteorology, and Jargon-Free AI Guidance
* **Track:** Agriculture & Rural Innovation
* **Event:** AI Conclave 2026 (Amal Jyothi College of Engineering)
* **Team:** Christy Varghese & Team
* **One-Line Pitch:** "Transforming complex agronomic data, weather forecasts, and seed pricing into simple, actionable daily farming decisions."

---

## Slide 2: The Problem
* **Slide Title:** Why Do 60%+ of First-Time Farmers Struggle or Quit?
* **Key Pain Points:**
  1. **Seed Price Gouging & Fraud:** Beginners often pay 2x–4x markups for uncertified, spurious seeds at private retail shops because they do not know fair market rates.
  2. **Unpredictable Weather Risks:** Sowing right before an unseasonal cloudburst or torrential downpour rots seedlings (damping-off wilt) and washes away topsoil.
  3. **Dense Academic Jargon:** Soil health cards, NPK ratios (kg/ha), and University extension bulletins are written in academic scientific terms that beginners cannot easily interpret.
  4. **Fragmented Ecosystem:** Weather is in one app, mandi prices in another, university calendars in PDFs, and government schemes on slow portals.

---

## Slide 3: The Solution — FarmStart
* **Slide Title:** A Unified, Intelligent Agricultural Decision Engine
* **Core Philosophy:** Clean, transparent, end-to-end guidance with zero agronomic jargon.
* **Three Pillars of FarmStart:**
  1. **Biological Matchmaking:** Scikit-Learn Machine Learning scoring soil, climate, and crop fit (0–100%).
  2. **Dynamic Meteorological Sowing Window:** Real-time 7-day weather forecasting (Open-Meteo) combined with Kerala Agricultural University (KAU) crop calendars to issue `SAFE`, `CAUTION`, or `UNSAFE` alerts.
  3. **Economic Transparency & AI Copilot:** Official KSSDA seed benchmarks, Agmarknet mandi rates, and a high-speed Groq LLM agent providing 3 concrete next steps.

---

## Slide 4: System Architecture & Data Pipeline
* **Slide Title:** How FarmStart Works (Architecture)
* **Diagram Flow:**
  - **Frontend Layer:** Responsive Single-Page Application (HTML5, TailwindCSS, FontAwesome) featuring dynamic farmer profiles and regional crop catalogs.
  - **API Gateway:** FastAPI Backend running asynchronous endpoints (`port 8000`), CORS-enabled, and OpenAPI Swagger documentation.
  - **Intelligence Engines:**
    - `ml_service.py`: Scikit-Learn Random Forest Classifier (`suitability_model.pkl`).
    - `weather_service.py`: Open-Meteo live API (rainfall mm, temp, humidity).
    - `sowing_service.py`: University calendar rule engine.
    - `price_service.py`: KSSDA fair seed benchmarks + Agmarknet mandi scraper.
    - `llm_service.py`: Groq Cloud LPU (`qwen/qwen3.8-27b`) streaming structured JSON advice.
  - **Persistence Layer:** SQLite relational database (`farmstart.db`) seeded with all 14 Kerala districts, soil health baselines, and certified crop varieties.

---

## Slide 5: Machine Learning Soil-Crop Suitability
* **Slide Title:** Predictive Biological Matching with Scikit-Learn
* **Model:** Random Forest Classifier trained on agro-climatic datasets.
* **10 Features Analyzed:**
  - `crop` (Tomato, Cardamom, Black Pepper, Rice, Banana, Ginger, Tapioca, Okra, Chilli)
  - `district` (14 Kerala agro-ecological zones)
  - `soil_type` (Hill soil, Laterite, Red loam, Coastal alluvium, Black soil)
  - `soil_ph` (Acidity / Alkalinity)
  - `nitrogen (N)`, `phosphorus (P)`, `potassium (K)` (kg/ha)
  - `temperature (°C)`, `humidity (%)`, `rainfall (mm)`
* **Intelligent Auto-Fill:** If a beginner doesn't know their soil NPK, the system automatically pulls official KAU baseline soil surveys for their specific district.
* **Composite Suitability Formula:**
  $$\text{Score} = (P_{\text{High}} \times 92.0) + (P_{\text{Medium}} \times 65.0) + (P_{\text{Low}} \times 35.0)$$
  - High Suitability (75–100%): Optimal biological match.
  - Medium (50–74%): Requires soil amendments / organic manure.
  - Low (<50%): Unsuitable terrain / severe climate risk.

---

## Slide 6: Real-Time Meteorology & Sowing Window
* **Slide Title:** Preventing Crop Failure with Live Weather Intelligence
* **Live Weather Engine:** Open-Meteo API queries live high-resolution coordinates for any Kerala district (zero API key bottleneck).
* **Evaluation Matrix:**
  - **Precipitation Threat:** If 7-day rainfall > 120 mm, trigger warning for root wash-out and damping-off fungal wilt.
  - **Drought Threat:** If 7-day rainfall < 10 mm, prompt drip irrigation and nursery mulching.
  - **Thermal Extremes:** Verifies germination temperature thresholds (e.g., tomato 16°C – 32°C).
* **Calendar Cross-Referencing:** Compares current date against official seasonal windows (e.g., Tomato: Sept 15 – Nov 30).
* **Visual Safety Status:**
  - 🟢 `SAFE TO SOW NOW` (Green badge)
  - 🟡 `PROCEED WITH CAUTION` (Amber badge — raised beds required)
  - 🔴 `SOWING NOT RECOMMENDED` (Red badge — outside planting window)

---

## Slide 7: Seed Price Transparency & Mandi Rates
* **Slide Title:** Protecting Farmers from Retail Gouging
* **The Problem:** Private vendors exploit new farmers with exaggerated seed prices.
* **The FarmStart Benchmark:**
  - Aggregates verified seed rates from **KSSDA (Kerala State Seed Development Authority)** and e-NAM.
  - Informs the farmer of certified fair benchmarks (e.g., Tomato PKM-1: ₹350 – ₹450 / 100g).
  - Displays certified university varieties (e.g., PKM-1, Vellayani Vijay, Akshaya F1).
* **Live Agmarknet Mandi Integration:** Connects with `data.gov.in` official agricultural market feeds for wholesale commodity produce pricing across Kerala markets.

---

## Slide 8: Conversational AI Copilot (Groq LPU)
* **Slide Title:** Jargon-Free Guidance with Groq LPU
* **Model:** `qwen/qwen3.8-27b` hosted on Groq’s Language Processing Unit (~500 tokens/sec ultra-low latency).
* **Contextual Prompt Injection:** Injects farmer name, district, crop, ML score, 7-day weather, and seed prices into the system prompt.
* **What the LLM Delivers:**
  1. Warm, empathetic greeting addressing the farmer by name.
  2. Clear non-technical explanation of current soil and weather conditions.
  3. **3 Specific Field Action Steps** (e.g., 15–20 cm raised beds, Trichoderma cow dung enrichment, 60 cm row spacing).
  4. Suggested follow-up prompt chips for interactive exploration.
  5. Local **Krishi Bhavan** subsidy reminders.

---

## Slide 9: Live Demo Scenario — The Anil in Idukki Story
* **Slide Title:** User Story & Live Demonstration
* **Persona:** Anil, a first-time farmer in Idukki with 0.5 acres of hill soil.
* **User Flow in FarmStart:**
  1. Anil opens FarmStart (`/app/`) and enters his name.
  2. Selects **District: Idukki** and **Crop: Tomato**.
  3. Clicks **"Get Advisory"**:
     - **ML Score:** `88% High Suitability` (Yield: 22–28 tonnes/ha).
     - **Weather:** `Safe to Sow` (Moderate rain ~28 mm, 23.5°C).
     - **Seed Benchmark:** Fair rate ₹350 – ₹450 / 100g (PKM-1).
  4. **AI Copilot Answers:** Explains how to construct raised beds to prevent monsoon puddling, advises where to procure certified seeds, and reminds him of the **Subhiksha Keralam** subsidy.

---

## Slide 10: Technical Stack & Implementation Highlights
* **Slide Title:** Technology Stack & Quality Engineering
* **Backend:** Python 3.12, FastAPI, Uvicorn, SQLAlchemy, SQLite, Pydantic v2.
* **Machine Learning:** Scikit-Learn (Random Forest Classifier, LabelEncoder, Joblib).
* **AI & LLM:** Groq Cloud SDK (`qwen/qwen3.8-27b`), JSON mode, custom error logging.
* **APIs:** Open-Meteo Meteorology, data.gov.in Agmarknet Mandi.
* **Frontend:** HTML5, Modern Vanilla JS, TailwindCSS, FontAwesome 6.
* **Assets:** 9 verified local botanical crop photos (0ms load latency, 100% offline).
* **Testing:** 100% automated pytest coverage across all 8 API endpoints.

---

## Slide 11: Government Scheme Integration & Social Impact
* **Slide Title:** Unlocking Real-World Financial Benefits
* **Direct Scheme Awareness:**
  - **Subhiksha Keralam Mission:** Up to ₹30,000 / hectare assistance for fallow land vegetable farming.
  - **PM-KISAN:** ₹6,000 / year direct income support.
  - **PMFBY:** 1.5% low-premium crop insurance for horticultural crops.
  - **State Horticulture Mission (SHM):** Up to 50% capital subsidy for drip irrigation and polyhouses.
  - Direct portal link to **Kerala AIMS (Agricultural Information Management System)**.
* **Social Impact:** Democratizes agricultural knowledge, prevents input cost exploitation, and lowers barrier of entry for educated youth entering farming.

---

## Slide 12: Future Roadmap & Conclusion
* **Slide Title:** What's Next for FarmStart?
* **Future Enhancements:**
  1. **Malayalam Voice Assistant:** Multilingual speech-to-text (Whisper) and text-to-speech for farmers who prefer audio interactions.
  2. **Computer Vision Leaf Doctor:** Camera photo upload using MobileNet/YOLO to diagnose leaf blight, powdery mildew, and nutrient deficiencies.
  3. **IoT Soil Sensor Sync:** Automatic BLE/LoRaWAN connection with on-field soil moisture and NPK probes.
  4. **Pan-India Expansion:** Expanding baseline agro-climatic calendars to Karnataka, Tamil Nadu, and Maharashtra.
* **Summary Statement:** "FarmStart turns uncertainty into confidence, giving every new cultivator a university professor, weather station, and market expert right in their pocket."

---

## Slide 13: Q&A & Demonstration Links
* **Live Web App:** http://127.0.0.1:8000/app/
* **Swagger API Documentation:** http://127.0.0.1:8000/docs
* **GitHub Repository:** https://github.com/christyvarghesetech/FarmStart
* **Thank You!** Questions from the Jury & Evaluators.
