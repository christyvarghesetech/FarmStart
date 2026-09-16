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
    Conversational agricultural copilot using Groq LLM to answer farmer queries
    dynamically with field context (weather, ML suitability, seed benchmark).
    """
    has_history = bool(conversation_history and len(conversation_history) > 0)
    crop_title = (context.crop or "crop").replace('_', ' ').title()
    district_title = (context.district or "your district").title()

    system_prompt = f"""You are FarmStart Copilot, an empathetic, expert agricultural AI assistant for new and smallholder farmers in Kerala, India.

BACKGROUND CONTEXT FOR THIS FARMER:
- Farmer Name: {farmer_name}
- District: {district_title}, Kerala
- Active Crop: {crop_title}
- Soil Type: {context.soil_type}
- ML Suitability: {context.suitability_category} ({context.suitability_score}/100)
- Sowing Window Status: {"Safe / Active Window" if context.is_safe_to_sow else "Outside Optimal Window"}
- Fair Seed Price Benchmark: {context.seed_price_range}
- 7-Day Weather Forecast: {context.weather_forecast}

CRITICAL CONVERSATIONAL RULES:
1. Answer the farmer's specific question directly, concisely, and practically with agricultural precision for Kerala conditions.
2. {"This is an ONGOING conversation. DO NOT repeat greetings ('Hello Farmer...'), do NOT introduce yourself again, and do NOT repeat the general sowing window, suitability score, or seed price unless specifically asked about them." if has_history else f"Address {farmer_name} warmly once and directly address their inquiry."}
3. Use the weather, soil, and suitability context as intelligent background knowledge (e.g. if the farmer asks about fertilizers or watering during high rainfall, caution against nutrient leaching or advise on drainage).
4. If the user's question contains Malayalam script or requests Malayalam, respond COMPLETELY in natural, fluent Malayalam (including reply, tips, and followups).
5. Provide 2-3 specific, realistic actionable tips tailored strictly to what was asked.
6. Provide 2 short, logical follow-up questions directly related to this topic.

RESPONSE FORMAT:
Strictly output a valid JSON object without markdown code fences:
{{
  "reply": "<Direct, helpful, non-repetitive response answering the user's question in plain language>",
  "actionable_tips": [
    "<Specific tip 1>",
    "<Specific tip 2>",
    "<Specific tip 3>"
  ],
  "suggested_followups": [
    "<Relevant follow-up 1>",
    "<Relevant follow-up 2>"
  ]
}}"""

    if settings.GROQ_API_KEY:
        try:
            client = Groq(api_key=settings.GROQ_API_KEY)
            
            messages = [{"role": "system", "content": system_prompt}]
            if conversation_history:
                for msg in conversation_history[-6:]:
                    role = "user" if msg.role in ("user", "farmer") else "assistant"
                    messages.append({"role": role, "content": msg.content})
            messages.append({"role": "user", "content": question})

            completion = client.chat.completions.create(
                model=settings.GROQ_MODEL,
                messages=messages,
                temperature=0.55,
                max_tokens=900,
                response_format={"type": "json_object"}
            )

            raw_text = completion.choices[0].message.content.strip()
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

    # Intelligent fallback adapted to question intent
    q_lower = (question or "").lower()
    is_malayalam = any('\u0d00' <= char <= '\u0d7f' for char in question)

    if any(w in q_lower for w in ["fertilizer", "manure", "npk", "urea", "potash", "compost", "ph", "വളം", "മണ്ണ്"]):
        if is_malayalam:
            reply = f"{crop_title} കൃഷിക്ക് {district_title} മേഖലയിലെ {context.soil_type} മണ്ണിൽ അടിവളമായി ജൈവവളവും (കമ്പോസ്റ്റ്/ചാണകം) നടീലിനു ശേഷം ആവശ്യാനുസരണം NPK വളങ്ങളും നൽകാം. മഴക്കാലമായതിനാൽ നൈട്രജൻ വളങ്ങൾ അധികമാകാതെ ശ്രദ്ധിക്കുക."
            actionable_tips = [
                "നടീലിന് മുൻപ് അടിവളമായി നന്നായി ഉണങ്ങിയ ചാണകപ്പൊടിയോ കമ്പോസ്റ്റോ ചേർക്കുക.",
                "മഴയുള്ളപ്പോൾ നൈട്രജൻ വളം കുറച്ച് നൽകുക, വേരുകൾക്ക് ബലം നൽകാൻ ഫോസ്ഫറസ്, പൊട്ടാഷ് എന്നിവ നൽകുക.",
                "കൃത്യമായ അളവിന് അടുത്തുള്ള കൃഷിഭവനിലെ കൃഷി ഓഫീസറുടെ നിർദ്ദേശം തേടുക."
            ]
            suggested_followups = [
                f"{crop_title} കൃഷിക്ക് ജൈവ കീടനാശിനികൾ ഏതെല്ലാം?",
                "കൃഷിഭവനിൽ നിന്ന് ലഭിക്കുന്ന സബ്‌സിഡികൾ എന്തൊക്കെ?"
            ]
        else:
            reply = f"For {crop_title} in {district_title} ({context.soil_type}), incorporate well-rotted compost as a basal dressing. For top-dressing, apply balanced NPK (19:19:19). Given current weather ({context.weather_forecast}), avoid heavy urea application to prevent leaching."
            actionable_tips = [
                f"Mix 2-3 kg organic compost per square meter into raised beds before planting {crop_title}.",
                "Apply split doses of NPK after 15 and 30 days to avoid rain runoff.",
                "Check soil pH at your local Krishi Bhavan to optimize nutrient absorption."
            ]
            suggested_followups = [
                f"What are common pest threats for {crop_title}?",
                f"How often should I water {crop_title} with current rain?"
            ]
    elif any(w in q_lower for w in ["pest", "disease", "insect", "rot", "wilt", "blight", "കീട", "രോഗ"]):
        if is_malayalam:
            reply = f"{district_title} കാലാവസ്ഥയിൽ {crop_title} കൃഷിയിൽ വേരുചീയലും ഇലപ്പുള്ളി രോഗങ്ങളും തടയാൻ നീർവാർച്ച ഉറപ്പാക്കുകയും വേപ്പെണ്ണ വെളുത്തുള്ളി മിശ്രിതം തളിക്കുകയും ചെയ്യുക."
            actionable_tips = [
                "രോഗബാധ തടയാൻ സ്യൂഡോമോണസ് 20 ഗ്രാം ഒരു ലിറ്റർ വെള്ളത്തിൽ കലക്കി തളിക്കുക.",
                "വെള്ളക്കെട്ട് ഒഴിവാക്കാൻ വാരങ്ങൾ ഉയർത്തി തടമെടുക്കുക.",
                "രോഗബാധിതമായ ഇലകൾ യഥാസമയം പറിച്ച് നശിപ്പിക്കുക."
            ]
            suggested_followups = [
                "ജൈവ കീടനാശിനികൾ എങ്ങനെ വീട്ടിൽ തയ്യാറാക്കാം?",
                "കൃഷിഭവനിൽ സ്യൂഡോമോണസ് ലഭ്യമാണോ?"
            ]
        else:
            reply = f"In {district_title}'s climate, watch for early blight, wilt, and sucking pests on {crop_title}. Maintain good spacing and avoid overhead watering to prevent fungal spread."
            actionable_tips = [
                "Spray Pseudomonas fluorescens (20g/L) fortnightly as a preventive bio-agent.",
                "Use 2% neem oil-garlic emulsion against sucking pests.",
                "Ensure ridges are elevated to prevent damp conditions around the stem."
            ]
            suggested_followups = [
                "How to prepare neem oil emulsion?",
                "Where can I buy certified biocontrol agents?"
            ]
    else:
        status_str = "an optimal window" if context.is_safe_to_sow else "requiring caution due to weather"
        reply = (
            f"Regarding {crop_title} in {district_title}: Conditions are currently {status_str}. "
            f"Suitability is rated {context.suitability_category} ({context.suitability_score}/100) with upcoming forecast: {context.weather_forecast}. "
            f"Fair certified seed rate is {context.seed_price_range}."
        )
        actionable_tips = [
            f"Prepare elevated beds with proper drainage channels for {crop_title}.",
            f"Procure certified KAU-recommended seed varieties within {context.seed_price_range}.",
            "Incorporate organic manure and Trichoderma before sowing."
        ]
        suggested_followups = [
            f"What fertilizer schedule should I follow for {crop_title}?",
            f"What government subsidies are available for {crop_title}?"
        ]

    return {
        "farmer_name": farmer_name,
        "reply": reply,
        "actionable_tips": actionable_tips,
        "suggested_followups": suggested_followups
    }
