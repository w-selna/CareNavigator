from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from pydantic import BaseModel
import json


class ReadJson():
    def __init__(self):
        self.list_of_providers=[]
        self.list_of_dicts=[]
    def init_json(self):
        with open('providers_name.json', 'r') as f:
            self.list_of_dicts = json.load(f)
    def reading_items(self):
        for items in self.list_of_dicts:
            self.list_of_providers.append(items['Provider Type'])
        return(self.list_of_providers)
    def create_list(self):
        self.init_json()
        return(self.reading_items())

#For structured response generation
class FormatOutput(BaseModel):
    diagnosis: str
    specialty: str
    
def diagnose_patient(patient_info: str) -> str:
    f"""
    Simulates a diagnosis process based on patient data.

    Args:
        {patient_info} includes:
          symptoms (list): A list of symptoms reported by the patient.
          age (int): The age of the patient.
          gender (str): The gender of the patient (e.g., 'male', 'female', 'other').

    Returns:
        str: one diagnosis with no more than three words.
        
    """

def provider_specialty(diagnosis: str) -> str:  
    f"""
    Searches for specialty to MATCH the diagnosis from the function --> diagnose_patient.

    Args:
        Diagnosis includes:
          str: diagnosis: {diagnosis}

    Returns:
        str: One specialty from the following list that matches the diagnosis for treatment: {ReadJson().create_list()}
    """

SYSTEM_INSTRUCTIONS = """
You are a helpful medical assistant. Your main task is to provide a diagnosis based on the 
patient's provided information.

MANDATORY: SUGGEST ONLY ONE MEDICAL CONDITION WITH NO ADDITIONAL EXPLANATIONS.
 
After providing the diagnosis, you must suggest ONE medical specialty from the provided list.

MANDATORY: SUGGEST ONLY ONE SPECIALTY, WITHOUT ADDITIONAL EXPLANATIONS, AND DO NOT MAKE UP ANY ANSWERS.
"""


diagnosis_agent = Agent(
    model=LiteLlm(model="openai/gpt-4o"),
    name='diagnosis_agent',
    description='An agent that provides possible diagnoses based on symptoms, age, and gender.',
    instruction=SYSTEM_INSTRUCTIONS,
    tools=[diagnose_patient,provider_specialty]
)

# Root agent to start execution if needed
root_agent = diagnosis_agent


