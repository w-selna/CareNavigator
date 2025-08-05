from google.adk.agents import Agent
from diagnosis_agent.agent import diagnosis_agent # uncomment once sub agent once it is up and running.
#from maps_agent.agent import maps_agent
from search_agent.agent import search_agent
from google.adk.models.lite_llm import LiteLlm

root_agent = Agent(
    model=LiteLlm(model="openai/gpt-4o"),
    name='root_agent',
    description='The Core User Facing Agent of CareNavigator', 
    instruction=
    """
    You are a medical triage agent. There are your responsabilities.
        - Assess the patient's symptoms, medical history and demographics. If after being asked for this information they do not tell you some parts of it, work with incomplete information.
        - Diagnose the patient based on their symptoms and assign a medical specialty for that condition.
        - Find a doctor that can treat the patient's condition.
    """,
    sub_agents=[diagnosis_agent, search_agent]
)
