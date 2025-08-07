from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from pydantic import BaseModel
import json


class ReadJson():
    def __init__(self):
        self.list_of_providers=[]
        self.list_of_dicts=[]
    def init_json(self):
        with open('/home/labadmin/Documents/agentic-ai/CareNavigator/diagnosis_agent/providers_name.json', 'r') as f:
            self.list_of_dicts = json.load(f)
    def reading_items(self):
        for items in self.list_of_dicts:
            self.list_of_providers.append(items['Provider Type'])
        return(self.list_of_providers)
    def create_list(self):
        self.init_json()
        return(self.reading_items())

#For structured response generation
class DiagnosisOutput(BaseModel):
    diagnosis: str
    specialty: str
# this is to cover cases  Family Medicine/  Internal Medicine
list_of_specialties=ReadJson().create_list()

SYSTEM_INSTRUCTIONS = f"""
You are a helpful medical assistant. Your main task is to provide a diagnosis based on the 
patient's symptoms.

MANDATORY: SUGGEST ONLY ONE MEDICAL CONDITION.

After providing the diagnosis, you must suggest ONE medical specialty from below that can treat the patient's condition.

{list_of_specialties}

MANDATORY: SUGGEST ONLY ONE SPECIALTY, WITHOUT ADDITIONAL EXPLANATIONS, AND DO NOT MAKE UP ANY ANSWERS.
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
    instruction='''Display diagnosis for patient's symptoms and suggest medical specialty who can treat the patient based on the
    information below. Inform the user that these are preliminary diagnosis only.

    {diagnosis}
    
    End with: Would you like me to assist you with finding the provider?    
    '''
    
    ,
    
)



