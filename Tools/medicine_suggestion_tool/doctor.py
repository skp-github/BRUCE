from langchain_openai import AzureChatOpenAI

from .query_template import (
    MODEL_PROMPT,
    PERSONA
)
from .schema import Prescription
from .utils import (
    get_azure_api_key,
    get_llm_model_name,
    get_llm_model_temperature,
    get_azure_api_version,
    get_prompt_examples
)

class Doctor() :
    """
    Main class that builds the prescription from the user problem and the medicines available
    """
    
    __slots__ = ("medicines", "model")
    
    def __init__(self, medicines : dict) :
        """
        Intializer that initializes the Doctor class.
        
        Args :
            medicines (dict) : The medicines available to the doctor.
        """
        self.medicines = medicines
        self.model = AzureChatOpenAI(
            azure_deployment=get_llm_model_name(),
            api_version=get_azure_api_version(),
            api_key=get_azure_api_key(),
            temperature=get_llm_model_temperature()
        )
        
    def build_prompt(self) -> str :
        """
        Helper function to build the prompt to the model
        
        Return :
            str : The prompt for the language model
        """
        prompt = MODEL_PROMPT.format(PERSONA = PERSONA,
                                     MEDICINE_INVENTORY = self.medicines,
                                     OUTPUT_SCHEMA = Prescription.model_json_schema())
        return prompt

            
    def model_output(self, user_prompt: str) -> object:
        """
        Helper function that sets up the language model to be used.
        
        Input :
            user_prompt (str) : The input query of the user
            
        Returns : 
            object : The language model to be queried.
        """
        
        system_prompt = [
            (
                "system",self.build_prompt()
            )
        ]
        user_input = [
            (
                "user", user_prompt
            )
        ]
        prompt_array = system_prompt + get_prompt_examples() + user_input
        self.model = self.model.with_structured_output(Prescription)
        output = self.model.invoke(input= prompt_array)
        prescription = output.dict()
        return prescription
        
    def build_prescription(self, user_input: str) -> dict:
        """
        Queries the language model to generate the daignosis and process it if required.
        
        Input : 
            user_input (str) : The input query of the user.
            
        Returns :
            dict : The generated diagnosis from the language model.
        """
        prescription = self.model_output(user_prompt = user_input)
        return prescription