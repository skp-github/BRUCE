from typing import Literal
from pydantic import BaseModel, Field

class Ingredient(BaseModel) :
    Item : str = Field(..., description="The name of the ingredient used.")
    Quantity : int = Field(..., description="The quantity of the food item used")
    Unit : Literal["g", "mL"] = Field(..., description="The unit of the quantity of ingredient used.")
    
class MEAL(BaseModel) :
    Name : str = Field(..., description="A name for the recipe. Should be shprt and funny")
    Ingredients : list[Ingredient] = Field(..., description="A list of the ingredients used in the recipe")
    Instructions : list[str] = Field(..., description="A list of sequential steps that are meant to be followed to prepare the recipe")   

