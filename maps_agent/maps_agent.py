import json
import os
import asyncio
import googlemaps
from typing import Dict, Any
from dotenv import load_dotenv

# Import Google ADK components
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm

# Load environment variables
load_dotenv()

# Initialize Google Maps client
gmaps = googlemaps.Client(key=os.getenv("GOOGLE_MAPS_API_KEY"))


# --- Tool function for ADK ---
def rerank_doctors_by_distance(patient_address: str) -> str:
    """
    Rerank doctors by driving distance to the patient's address.

    Args:
        patient_address: The user's full address or general location.

    Returns:
        str: Formatted string with top 3 doctors ranked by distance.
    """
    try:
        with open("doctor_data.json", "r") as f:
            doctors = json.load(f)
    except Exception as e:
        return f"Error loading doctors: {e}"

    ranked = []
    for doc in doctors:
        try:
            result = gmaps.distance_matrix(
                origins=[patient_address],
                destinations=[doc["address"]],
                mode="driving",
                units="imperial"
            )
            miles_text = result["rows"][0]["elements"][0]["distance"]["text"]
            miles = float(miles_text.replace("mi", "").replace(",", "").strip())
            doc["distance"] = miles
            ranked.append(doc)
        except Exception as e:
            print(f"Error calculating distance for {doc.get('name', 'Unknown')}: {e}")
            continue

    # Get top 3 closest doctors
    top_doctors = sorted(ranked, key=lambda d: d["distance"])[:3]

    if not top_doctors:
        return "No doctors found within reasonable distance."

    return "\n".join(
        f"{doc['name']} – {doc['distance']} mi – "
        f"{doc.get('experience', '?')} yrs – rated {doc.get('score', '?')}"
        for doc in top_doctors
    )


# --- Tool schema for OpenAI function calling (ADK compatible) ---
distance_tool = {
    "type": "function",
    "function": {
        "name": "rerank_doctors_by_distance",
        "description": "Rerank doctors by driving distance to the patient's address. The list of doctors are given",
        "parameters": {
            "type": "object",
            "properties": {
                "patient_address": {
                    "type": "string",
                    "description": "The user's full address or general location."
                }
            },
            "required": ["patient_address"]
        }
    }
}

# --- ADK Agent Definition with OpenAI via LiteLLM ---
maps_agent = Agent(
    name="maps_agent",
    model=LiteLlm(model="gpt-4o"),  # Use OpenAI GPT-4o via LiteLLM
    instruction="""You are a helpful medical assistant that finds doctors near patients. 
    When a user provides their location, use the rerank_doctors_by_distance tool to find the 
    closest doctors. 

    Always be helpful and provide clear, formatted information about the doctors including:
    - Doctor name
    - Distance from patient
    """,
    description="An agent that helps patients find nearby doctors ranked by distance.",
    tools=[rerank_doctors_by_distance]
)

# --- Root Agent (this is the main agent definition) ---
root_agent = maps_agent