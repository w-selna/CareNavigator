
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
    instruction=
        '''You are an expert insurance matching assistant. 
        Your task is to determine if a patient's insurance is accepted by a doctor. 
        The user will provide the doctor's accepted insurance plans and the patient's plan. 
        When checking, be flexible with plan variations (e.g., 'Blue Cross' matches 'Blue Cross Blue Shield'). 
        However, do not assume unrelated plans are compatible (e.g., 'Blue Cross' is not a match for 'Blue Shield of California'). 
        Provide a concise, direct reason for the match or non-match. '''
)
