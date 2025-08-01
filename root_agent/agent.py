from google.adk.agents import Agent
from diagnosis_agent.agent import diagnosis_agent
from maps_agent.agent import maps_agent
from search_agent.agent import search_agent
from google.adk.models.lite_llm import LiteLlm

root_agent = Agent(
    model=LiteLlm(model="openai/gpt-4o"),
    name='root_agent',
    description='a good agent', #WS Note: This needs to be updated.
    instruction="You are a travel agent. Delegate tasks to sub-agents as needed.",#WS Note: This needs to be updated. A lot!
    sub_agents=[diagnosis_agent, maps_agent, search_agent]
)
