
import os
import json
import asyncio
from typing import Dict, Any

from google.adk.agents.llm_agent import Agent
from google.adk.models.lite_llm import LiteLlm
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.genai import types


async def check_insurance_match(params: Dict[str, Any]) -> Dict[str, Any]:
    if not params or "doctor_info" not in params or "patient_insurance" not in params:
        last_user_message = params.get("last_user_message", None)
        if isinstance(last_user_message, str):
            try:
                data = json.loads(last_user_message)
                doctor_info = data.get("doctor_info", {})
                patient_insurance = data.get("patient_insurance", "")
            except Exception:
                doctor_info, patient_insurance = {}, ""
        else:
            doctor_info, patient_insurance = {}, ""
    else:
        doctor_info = params.get("doctor_info", {})
        patient_insurance = params.get("patient_insurance", "")

    accepted_plans = doctor_info.get("insurance_plans", [])
    accepted_str = json.dumps(accepted_plans, indent=2)

    prompt = f"""
You are an expert insurance matching assistant.

Doctor accepts these insurance plans:
{accepted_str}

Patient insurance plan:
{patient_insurance}

Answer only with JSON in this format:
{{
  "acceptsInsurance": true or false,
  "reason": "explanation text"
}}
"""
    llm = LiteLlm(model="openai/gpt-4o", api_key=os.getenv("OPENAI_API_KEY"))
    response = await llm.chat_completion_async(
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
    )
    text = response.choices[0].message.content.strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return {
            "acceptsInsurance": False,
            "reason": "Could not parse LLM response as JSON.",
        }


insurance_agent = Agent(
    model=LiteLlm(model="openai/gpt-4o", api_key=os.getenv("OPENAI_API_KEY")),
    name="insurance_agent",
    description="Agent that checks if a doctor's insurance plans match patient's insurance.",
    instruction=(
        "Always call the 'check_insurance_match' tool using the session state values for 'doctor_info' "
        "and 'patient_insurance' when the user asks about insurance matching."
    ),
    tools=[check_insurance_match],
)

session_service = InMemorySessionService()
session = asyncio.run(session_service.create_session(
    app_name="insurance_app",
    user_id="user_1",
    session_id="session_1",
))
runner = Runner(
    agent=insurance_agent,
    app_name="insurance_app",
    session_service=session_service,
)

doctor_info = {
    "name": "Dr. Alice",
    "insurance_plans": ["Blue Cross", "United Healthcare", "Cigna PPO"],
}
patient_insurance = "Blue Shield of California"

user_message_text = json.dumps({
    "doctor_info": doctor_info,
    "patient_insurance": patient_insurance
})

async def main():
    user_content = types.Content(role="user", parts=[types.Part(text=user_message_text)])

    async for event in runner.run_async(
        user_id="user_1",
        session_id="session_1",
        new_message=user_content,
    ):
        if event.is_final_response():
            print("Agent final response:")
            print(event.content.parts[0].text)

if __name__ == "__main__":
    asyncio.run(main())