from google.adk.agents import Agent, SequentialAgent
from diagnosis_agent.agent import diagnosis_agent , display_diagnosis_agent# uncomment once sub agent once it is up and running.
#from maps_agent.agent import maps_agent
from search_agent.agent import search_agent
from google.adk.models.lite_llm import LiteLlm

root_agent = Agent(
    model=LiteLlm(model="openai/gpt-4o"),
    name='root_agent',
    description='The Core User Facing Agent of CareNavigator', 
    instruction="""
    You are a medical triage agent. There are your responsabilities.
        1. Assess the patient's symptoms, medical history and demographics. If after being asked for this information they do not tell you some parts of it, work with incomplete information.
        2. Diagnose the patient based on their symptoms and assign a medical specialty for that condition.
        3. Find a doctor that can treat the patient's condition. ALWAYS PROCEED TO 4 AFTER 3.
        4. Start a conversation with the diagnosis agent to collaboratively select the best doctor for the condition.

        

        MANDATORY:
        - Continue the conversation until you and the diagnosis agent agree OR a maximum of 3 message exchanges (whichever comes first).
        - Format all communication as shown in the example above.
        - Explicitly call the `diagnosis_agent` for their input when making doctor recommendations.  
    """,#,
    #sub_agents=[diagnosis_agent,  search_agent  ]
    sub_agents=[
        SequentialAgent(
            name='forecast_and_display_agent',
            description='An agent that uses the sub-agents to diagnose the paitients symptoms and display the diagnosis.',
            sub_agents=[diagnosis_agent, display_diagnosis_agent])
        ,  search_agent]
)
