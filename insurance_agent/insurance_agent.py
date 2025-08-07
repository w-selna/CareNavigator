
import os
import json
import asyncio
from typing import Dict, Any

from google.adk.agents.llm_agent import Agent
from google.adk.models.lite_llm import LiteLlm
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.genai import types


insurance_agent = Agent(
    model=LiteLlm(model="openai/gpt-4o", api_key=os.getenv("OPENAI_API_KEY")),
    name="insurance_agent",
    description="Agent that checks if a doctor's insurance plans match a patient's insurance and returns a JSON response.",
    instruction=(
        "You are an expert insurance matching assistant. "
        "Your task is to determine if a patient's insurance is accepted by a doctor. "
        "The user will provide the doctor's accepted insurance plans and the patient's plan. "
        "When checking, be flexible with plan variations (e.g., 'Blue Cross' matches 'Blue Cross Blue Shield'). "
        "However, do not assume unrelated plans are compatible (e.g., 'Blue Cross' is not a match for 'Blue Shield of California'). "
        "Provide a concise, direct reason for the match or non-match. "
        "Answer ONLY with JSON in this format: "
        '{"acceptsInsurance": true or false, "reason": "explanation text"}'
    ),
    tools=[],
)
'''
session_service = InMemorySessionService()

runner = Runner(
    agent=insurance_agent,
    app_name="insurance_app",
    session_service=session_service,
)

async def main():
    doctor_info = {
        "name": "Dr. Alice",
        "insurance_plans": ["Blue Cross", "United Healthcare", "Cigna PPO"],
    }
    patient_insurance = "UNH"

    user_message_text = (
        f"Doctor accepts these insurance plans: {doctor_info['insurance_plans']}. "
        f"Patient insurance plan: {patient_insurance}. "
        "Please check if they match."
    )

    session = await session_service.create_session(
        app_name="insurance_app",
        user_id="user_1",
        session_id="session_1",
    )

    user_content = types.Content(role="user", parts=[types.Part(text=user_message_text)])

    async for event in runner.run_async(
        user_id="user_1",
        session_id=session.id,
        new_message=user_content,
    ):
        if event.is_final_response():
            print("Agent final response:")
            print(event.content.parts[0].text)

if __name__ == "__main__":
    if os.getenv("OPENAI_API_KEY") is None:
        print("Please set the OPENAI_API_KEY environment variable.")
    else:
        asyncio.run(main())
'''
