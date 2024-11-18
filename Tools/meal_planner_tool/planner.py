from langchain_openai import AzureChatOpenAI

from .query_template import (
    MODEL_PROMPT,
    PERSONA
)
from .schema import MEAL
from .utils import (
    get_azure_api_key,
    get_llm_model_name,
    get_llm_model_temperature,
    get_azure_api_version
)

class MealPlanner() :
    """
    Main class that builds the meal from the ingredients and the nutrition
    """
    
    __slots__ = ("ingredient", "nutrition", "model")
    
    def __init__(self, ingredients : dict, nutrition : dict) :
        """
        Intializer that initializes the Planner class.
        
        Args :
            ingredients (dict) : The ingredients available to the planner.
            nutritiona (dict) : The nutritional targets for the day
        """
        self.ingredient = ingredients
        self.nutrition = nutrition
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
                                     GROCERY_INVENTORY = self.ingredient, 
                                     NUTRITIONAL_GOALS = self.nutrition, 
                                     OUTPUT_SCHEMA = MEAL.model_json_schema())
        return prompt

            
    def model_output(self, user_prompt: str) -> object:
        """
        Helper function that sets up the language model to be used.
        
        Input :
            user_prompt (str) : The inout query of the user
            
        Returns : 
            object : The language model to be queried.
        """
        
        prompt_array = [
            (
                "system",self.build_prompt()
            ),
            (
                "user", user_prompt
            )
        ]
        self.model = self.model.with_structured_output(MEAL)
        output = self.model.invoke(input= prompt_array).dict()
        return output
        
    def build_meal(self, user_input: str) -> dict:
        """
        Queries the language model to generate the meal and process it if required.
        
        Input : 
            user_input (str) : The input query of the user.
            
        Returns :
            dict : The generated query plan from the language model.
        """
        meal_plan = self.model_output(user_prompt = user_input)
        return meal_plan