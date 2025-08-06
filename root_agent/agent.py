from google.adk.agents import Agent, SequentialAgent
from diagnosis_agent.agent import diagnosis_agent , display_diagnosis_agent# uncomment once sub agent once it is up and running.
#from maps_agent.agent import maps_agent
from search_agent.agent import search_agent
from google.adk.models.lite_llm import LiteLlm

root_agent = Agent(
    model=LiteLlm(model="openai/gpt-4o"),
    name='root_agent',
    description='The Core User Facing Agent of CareNavigator', 
    instruction="Your name is Navi, a friendly care navigator AI agent for the company CareNavigator. Introduce yourself as such at the beginning of the chat. Consult with the user about their health issues and ask for more information from them as needed." \
    "You can use the sub-agents to help you with specific tasks." \
    "   If you need to diagnose the users ailments, use the diagnosis agent. Unless the patient is explicit about what they are diagnosed with, try not to scare the user by giving them exactly what disease they may have. Equivocate on your speculation to the user, but be more certain and specific when calling Agents and tools." \
    "   If you need to searchs for doctors to treat the user, use the search agent. Make a decision about the best doctor for the user based on ratings,proximity, and number of reviews." \
    "   If you need to find a location on a map or distances between places, use the maps agent." \
    "   If you need to review the insurance accepted by each doctor, use the JSON agent." \
    "Be empathetic and supportive in your responses."#,
    #sub_agents=[diagnosis_agent,  search_agent  ]
    sub_agents=[
        SequentialAgent(
            name='forecast_and_display_agent',
            description='An agent that uses sub-agents to get the weather forecast and then display it to the user.',
            sub_agents=[diagnosis_agent, display_diagnosis_agent])
        ,  search_agent]
)
