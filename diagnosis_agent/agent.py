from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from pydantic import BaseModel
import json



#For structured response generation
class DiagnosisOutput(BaseModel):
    diagnosis: str
    specialty: str



SYSTEM_INSTRUCTIONS = """

You are a helpful and precise medical assistant.

Your primary task is to provide a diagnosis based solely on the patient's symptoms. 

Use only the information given, do not infer or assume additional data.

MANDATORY:

    - Return **only one medical condition** as your diagnosis.
    - Then, recommend **only one medical specialty** that is appropriate for treating the diagnosed condition.

IMPORTANT RULES:

    - Do not provide explanations, justifications, or alternative options.
    - Ask for more information if needed.
    - Never make up a diagnosis or a specialty.

"""


diagnosis_agent = Agent(
    model=LiteLlm(model="openai/gpt-4o"),
    name='diagnosis_agent',
    description='An agent that provides possible diagnoses based on symptoms, age, and gender.',
    instruction=SYSTEM_INSTRUCTIONS,
    output_key='diagnosis',
    output_schema=DiagnosisOutput
)

display_diagnosis_agent = Agent(
    model=LiteLlm(model="openai/gpt-4o"),
    name='display_diagnosis_agent',
    description='An agent that provides an explanation of diagnosis from using the structured output of diagnosis_agent.',
    instruction='''
    Display and explain diagnosis for patient's symptoms and suggestted medical specialty ONLY from the diagnosis agent's diagnosis listed below. 
    
    {diagnosis}

    Inform the user that these are preliminary diagnosis only to assist them finding the specialist AND THEY SHOULD SEE THE SPECIALIST.
    
    End with: Would you like me to assist you with finding the provider? 

    '''
        
)



