# distance_reranker_agent.py
from google.adk.agents import Agent
import googlemaps
import os
import json

gmaps = googlemaps.Client(key=os.getenv("Maps_API_KEY"))

def calculate_distance(patient_address: str, doctor_address: str) -> dict:
    try:
        result = gmaps.distance_matrix(
            origins=[patient_address],
            destinations=[doctor_address],
            mode="driving",
            units="imperial"
        )
        miles = result["rows"][0]["elements"][0]["distance"]["text"]
        return {"status": "success", "miles": miles}
    except Exception as e:
        return {"status": "error", "error_message": str(e)}

def rerank_doctors_by_distance(patient_address: str) -> dict:
    try:
        with open("doctors.json", "r") as f:
            doctors = json.load(f)
    except Exception as e:
        return {"status": "error", "error_message": f"Could not load doctor data: {str(e)}"}

    ranked = []
    for doc in doctors:
        result = calculate_distance(patient_address, doc["address"])
        if result["status"] == "success":
            miles = float(result["miles"].replace("mi", "").strip())
            doc["distance"] = miles
        else:
            doc["distance"] = float("inf")
        ranked.append(doc)

    # Sort and take top 3
    sorted_doctors = sorted(ranked, key=lambda d: d["distance"])[:3]

    output = "\n".join(
        f"{doc['name']} – {doc['distance']} mi – {doc.get('experience', '?')} yrs – rated {doc.get('score', '?')}"
        for doc in sorted_doctors
    )

    return {
        "status": "success",
        "report": "Here are the top 3 closest doctors:\n\n" + output
    }

# NOTE: The agent variable MUST be named `root_agent`.
root_agent = Agent(
    name="distance_reranker_agent",
    model="gpt-4o",  # OpenAI model
    description="Reranks doctors based on user preferences and distance from the patient.",
    instruction="You are an agent that finds nearby doctors based on preferences.",
    tools=[rerank_doctors_by_distance]
)