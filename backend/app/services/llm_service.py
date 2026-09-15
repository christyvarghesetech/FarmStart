import json
from typing import Dict, Any, List
from groq import Groq
from app.config import settings
from app.schemas.advisory import AdvisoryChatContext, ChatMessage


def generate_llm_advisory(
    farmer_name: str,
    question: str,
    context: AdvisoryChatContext,
    conversation_history: List[ChatMessage] = None
) -> Dict[str, Any]:
    """
    LLM conversational copilot using Groq (Llama 3.3 70B) to translate
    weather data, ML suitability, and seed benchmarks into accessible advice.
    """
    history_lines = []
    if conversation_history:
        for msg in conversation_history[-4:]: # last 4 exchanges
            role_label = "Farmer" if msg.role == "user" else "Copilot"
            history_lines.append(f"{role_label}: {msg.content}")

    history_text = "\n".join(history_lines) if history_lines else "No previous conversation."

    system_prompt = f"""
You are FarmStart Copilot, a friendly, knowledgeable, and empathetic agricultural assistant for new and first-time farmers in Kerala, India.

Your goal is to guide farmers with practical, non-technical, and actionable advice based on real meteorological, ML suitability, and price data.

FARMER & FIELD CONTEXT:
- Farmer Name: {farmer_name}
- District / Location: {context.district}, Kerala
- Intended Crop: {context.crop}
- Soil Type: {context.soil_type}
- ML Suitability Prediction: {context.suitability_category} (Score: {context.suitability_score}/100)
- Safe to Sow Currently: {"Yes - Active Safe Window" if context.is_safe_to_sow else "Caution / Outside Optimal Window"}
- Fair Seed Price Benchmark: {context.seed_price_range}
- 7-Day Weather Forecast: {context.weather_forecast}

GUIDELINES:
1. Address the farmer warmly by name ({farmer_name}).
2. Answer their question directly in simple, clear everyday language (avoid heavy academic agronomy jargon).
3. Clearly state whether now is a good time to sow, citing the weather conditions and sowing calendar.
4. Mention the fair seed price range so they know what not to overpay at local retail shops.
5. Provide 3 specific, actionable steps (e.g. raised beds, seed treatment, drainage).
6. Remind them gently to check with their local Krishi Bhavan officer for subsidized inputs.

FORMAT YOUR RESPONSE EXACTLY AS A JSON OBJECT:
{{
  "reply": "<Your warm, comprehensive paragraph explaining the situation and recommendations in plain language>",
  "actionable_tips": [
    "<Actionable Tip 1>",
    "<Actionable Tip 2>",
    "<Actionable Tip 3>"
  ],
  "suggested_followups": [
    "<Short follow-up question the farmer might want to ask next>",
    "<Another relevant follow-up question>"
  ]
}}
Ensure the output is strictly valid JSON without any markdown code fence wrappers or backticks.
"""

    if settings.GROQ_API_KEY:
        try:
            client = Groq(api_key=settings.GROQ_API_KEY)
            user_prompt = f"""
Farmer's Question: "{question}"

Conversation Context:
{history_text}
"""
            completion = client.chat.completions.create(
                model=settings.GROQ_MODEL,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.3,
                max_tokens=900,
                response_format={"type": "json_object"}
            )

            raw_text = completion.choices[0].message.content.strip()
            # Clean possible markdown code fences
            if raw_text.startswith("```json"):
                raw_text = raw_text[7:]
            if raw_text.startswith("```"):
                raw_text = raw_text[3:]
            if raw_text.endswith("```"):
                raw_text = raw_text[:-3]
            raw_text = raw_text.strip()

            result_json = json.loads(raw_text)
            print(f"[FarmStart Copilot] Groq LLM ({settings.GROQ_MODEL}) response generated successfully.")

            return {
                "farmer_name": farmer_name,
                "reply": result_json.get("reply", ""),
                "actionable_tips": result_json.get("actionable_tips", []),
                "suggested_followups": result_json.get("suggested_followups", [])
            }

        except Exception as e:
            print(f"[FarmStart Copilot Warning] Groq API call error: {e}. Utilizing intelligent fallback.")

    # Intelligent fallback adapted to the specific crop and district
    crop_title = (context.crop or "crop").replace('_', ' ').title()
    district_title = (context.district or "your district").title()

    status_str = "advantageous" if context.is_safe_to_sow else "challenging"
    reply = (
        f"Hello {farmer_name}! Regarding your inquiry about {crop_title} in {district_title}: "
        f"Our machine learning model scored your conditions as {context.suitability_category} suitability "
        f"({context.suitability_score}/100). It is currently {status_str} for field sowing. "
        f"The upcoming forecast indicates {context.weather_forecast}. "
        f"For quality seeds, the fair market benchmark is {context.seed_price_range}; "
        f"always purchase certified seed stocks and avoid unverified markups."
    )

    actionable_tips = [
        f"Prepare well-draining soil beds or ridges suited for {crop_title} to protect root zones from moisture stress.",
        f"Procure certified {crop_title} seeds/planting material within the benchmark of {context.seed_price_range}.",
        f"Apply organic compost or Trichoderma-enriched manure prior to sowing to fortify against soil-borne pathogens."
    ]

    suggested_followups = [
        f"What fertilizer schedule should I follow for {crop_title}?",
        f"Are there government subsidies for {crop_title} in {district_title}?",
        f"Where is the nearest Krishi Bhavan in {district_title}?"
    ]

    return {
        "farmer_name": farmer_name,
        "reply": reply,
        "actionable_tips": actionable_tips,
        "suggested_followups": suggested_followups
    }
