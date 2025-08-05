import json
import os
import openai
import googlemaps
from dotenv import load_dotenv

load_dotenv()
openai_client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
gmaps = googlemaps.Client(key=os.getenv("GOOGLE_MAPS_API_KEY"))

# --- Tool function ---
def rerank_doctors_by_distance(patient_address: str) -> str:
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
            continue

    # Get top 3
    top_doctors = sorted(ranked, key=lambda d: d["distance"])[:3]

    return "\n".join(
        f"{doc['name']} – {doc['distance']} mi – "
        f"{doc.get('experience', '?')} yrs – rated {doc.get('score', '?')}"
        for doc in top_doctors
    )

# --- Tool schema for OpenAI function calling ---
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


# --- Root agent (via LLM call) ---
def run_agent(user_message: str):
    messages = [
        {
            "role": "system",
            "content": "You are a helpful agent that finds doctors near the user using a distance-based reranking tool. Ask the user's location if needed, then call the tool."
        },
        {
            "role": "user",
            "content": user_message
        }
    ]

    response = openai_client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        tools=[distance_tool],
        tool_choice="auto"
    )

    tool_call = response.choices[0].message.tool_calls[0]
    args = json.loads(tool_call.function.arguments)
    address = args["patient_address"]

    tool_result = rerank_doctors_by_distance(address)

    # Let GPT summarize the tool output (optional):
    messages.append({
        "role": "assistant",
        "tool_calls": [tool_call]
    })
    messages.append({
        "role": "tool",
        "tool_call_id": tool_call.id,
        "name": tool_call.function.name,
        "content": tool_result
    })

    final_response = openai_client.chat.completions.create(
        model="gpt-4o",
        messages=messages
    )

    print("\n📋 GPT Response:\n")
    print(final_response.choices[0].message.content)

# run_agent("I'm near Evanston, IL and looking for a doctor.")

if __name__ == "__main__":
    print("Type your request (e.g., 'I'm in Evanston, IL and want a spine specialist')\nType 'exit' to quit.\n")

    while True:
        user_input = input("You: ")
        if user_input.strip().lower() in {"exit", "quit"}:
            print("Goodbye!")
            break

        try:
            run_agent(user_input)
        except Exception as e:
            print(f"Error: {e}")
