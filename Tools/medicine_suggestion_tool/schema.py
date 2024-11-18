from pydantic import BaseModel, Field

class Medicine(BaseModel) :
    Name : str = Field(description="The name of the medicine that should be consumed.")
    Dosage : str = Field(description="The quantitity of the medicine that should be used.")
    Instruction : str = Field(description="How and when to use the medicine.")
    
class Prescription(BaseModel) :
    Diagnosis : str = Field (..., description="A short string explaining what can be the possible issue.")
    Medication : Medicine = Field(..., description="The suggested Medicines for the issue")
