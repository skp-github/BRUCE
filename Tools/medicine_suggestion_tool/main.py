"""
This is a medicine prescribing tool. Takes in the medicine inventory and gives diagnosis
"""


from .doctor import Doctor


def main(inventory : dict, user_input : str) -> dict :
    """
    Main entry point for the Medicine Suggestion tool.
    
    Args :
        inventory (dict) : All the medicines available in the inventory
        user_input (str) : The input prompt of the user
        
    Returns :
        dict : The suggested diagnosis.
    """
    
    try :
        # NOTE: Lazy checking for now, should be changed later
        if inventory == {} :
            raise ValueError("The inventory cannot be empty")
        
        # TODO: Check for proper schema for the inventory and the nutrition
                
        planner = Doctor(medicines=inventory)
        generated_prescription = planner.build_prescription(user_input=user_input)
        return generated_prescription
    except Exception as e:
        raise(e)
        
# if __name__ == "__main__" :
#     db = {
#   "inventory": {
#     "acetaminophen": {
#       "quantity": 1000,
#       "unit": "tablets",
#       "strength": "500mg",
#       "category": "pain_reliever"
#     },
#     "ibuprofen": {
#       "quantity": 800,
#       "unit": "tablets",
#       "strength": "200mg",
#       "category": "nsaid"
#     },
#     "amoxicillin": {
#       "quantity": 500,
#       "unit": "capsules",
#       "strength": "250mg",
#       "category": "antibiotic"
#     },
#     "omeprazole": {
#       "quantity": 300,
#       "unit": "tablets",
#       "strength": "20mg",
#       "category": "antacid"
#     },
#     "lisinopril": {
#       "quantity": 200,
#       "unit": "tablets",
#       "strength": "10mg",
#       "category": "blood_pressure"
#     },
#     "metformin": {
#       "quantity": 400,
#       "unit": "tablets",
#       "strength": "500mg",
#       "category": "diabetes"
#     },
#     "albuterol": {
#       "quantity": 50,
#       "unit": "inhalers",
#       "strength": "90mcg/actuation",
#       "category": "bronchodilator"
#     },
#     "insulin_regular": {
#       "quantity": 100,
#       "unit": "vials",
#       "strength": "100units/ml",
#       "category": "diabetes"
#     },
#     "levothyroxine": {
#       "quantity": 250,
#       "unit": "tablets",
#       "strength": "50mcg",
#       "category": "thyroid"
#     },
#     "prednisone": {
#       "quantity": 150,
#       "unit": "tablets",
#       "strength": "5mg",
#       "category": "corticosteroid"
#     },
#     "sertraline": {
#       "quantity": 200,
#       "unit": "tablets",
#       "strength": "50mg",
#       "category": "antidepressant"
#     },
#     "diphenhydramine": {
#       "quantity": 300,
#       "unit": "capsules",
#       "strength": "25mg",
#       "category": "antihistamine"
#     },
#     "metoprolol": {
#       "quantity": 180,
#       "unit": "tablets",
#       "strength": "25mg",
#       "category": "beta_blocker"
#     },
#     "warfarin": {
#       "quantity": 100,
#       "unit": "tablets",
#       "strength": "5mg",
#       "category": "anticoagulant"
#     },
#     "fluticasone": {
#       "quantity": 75,
#       "unit": "nasal_sprays",
#       "strength": "50mcg/spray",
#       "category": "corticosteroid"
#     },
#     "amlodipine": {
#       "quantity": 240,
#       "unit": "tablets",
#       "strength": "5mg",
#       "category": "calcium_channel_blocker"
#     },
#     "gabapentin": {
#       "quantity": 300,
#       "unit": "capsules",
#       "strength": "300mg",
#       "category": "anticonvulsant"
#     },
#     "ciprofloxacin": {
#       "quantity": 150,
#       "unit": "tablets",
#       "strength": "500mg",
#       "category": "antibiotic"
#     },
#     "pantoprazole": {
#       "quantity": 180,
#       "unit": "tablets",
#       "strength": "40mg",
#       "category": "antacid"
#     },
#     "azithromycin": {
#       "quantity": 100,
#       "unit": "tablets",
#       "strength": "250mg",
#       "category": "antibiotic"
#     },
#     "loratadine": {
#       "quantity": 400,
#       "unit": "tablets",
#       "strength": "10mg",
#       "category": "antihistamine"
#     },
#     "tramadol": {
#       "quantity": 120,
#       "unit": "tablets",
#       "strength": "50mg",
#       "category": "pain_reliever"
#     },
#     "cephalexin": {
#       "quantity": 200,
#       "unit": "capsules",
#       "strength": "500mg",
#       "category": "antibiotic"
#     },
#     "alprazolam": {
#       "quantity": 100,
#       "unit": "tablets",
#       "strength": "0.5mg",
#       "category": "anxiolytic"
#     },
#     "escitalopram": {
#       "quantity": 180,
#       "unit": "tablets",
#       "strength": "10mg",
#       "category": "antidepressant"
#     },
#     "hydrochlorothiazide": {
#       "quantity": 200,
#       "unit": "tablets",
#       "strength": "25mg",
#       "category": "diuretic"
#     },
#     "metronidazole": {
#       "quantity": 150,
#       "unit": "tablets",
#       "strength": "500mg",
#       "category": "antibiotic"
#     },
#     "losartan": {
#       "quantity": 180,
#       "unit": "tablets",
#       "strength": "50mg",
#       "category": "blood_pressure"
#     },
#     "furosemide": {
#       "quantity": 120,
#       "unit": "tablets",
#       "strength": "40mg",
#       "category": "diuretic"
#     },
#     "duloxetine": {
#       "quantity": 160,
#       "unit": "capsules",
#       "strength": "30mg",
#       "category": "antidepressant"
#     },
#     "venlafaxine": {
#       "quantity": 150,
#       "unit": "capsules",
#       "strength": "75mg",
#       "category": "antidepressant"
#     },
#     "budesonide": {
#       "quantity": 60,
#       "unit": "inhalers",
#       "strength": "160mcg/actuation",
#       "category": "corticosteroid"
#     },
#     "montelukast": {
#       "quantity": 180,
#       "unit": "tablets",
#       "strength": "10mg",
#       "category": "antiasthmatic"
#     },
#     "ranitidine": {
#       "quantity": 200,
#       "unit": "tablets",
#       "strength": "150mg",
#       "category": "antacid"
#     },
#     "clonazepam": {
#       "quantity": 90,
#       "unit": "tablets",
#       "strength": "0.5mg",
#       "category": "anticonvulsant"
#     },
#     "amitriptyline": {
#       "quantity": 120,
#       "unit": "tablets",
#       "strength": "25mg",
#       "category": "antidepressant"
#     },
#     "atorvastatin": {
#       "quantity": 180,
#       "unit": "tablets",
#       "strength": "20mg",
#       "category": "statin"
#     },
#     "rosuvastatin": {
#       "quantity": 150,
#       "unit": "tablets",
#       "strength": "10mg",
#       "category": "statin"
#     },
#     "simvastatin": {
#       "quantity": 160,
#       "unit": "tablets",
#       "strength": "20mg",
#       "category": "statin"
#     },
#     "citalopram": {
#       "quantity": 140,
#       "unit": "tablets",
#       "strength": "20mg",
#       "category": "antidepressant"
#     },
#     "naproxen": {
#       "quantity": 200,
#       "unit": "tablets",
#       "strength": "500mg",
#       "category": "nsaid"
#     },
#     "carvedilol": {
#       "quantity": 120,
#       "unit": "tablets",
#       "strength": "12.5mg",
#       "category": "beta_blocker"
#     },
#     "doxycycline": {
#       "quantity": 100,
#       "unit": "capsules",
#       "strength": "100mg",
#       "category": "antibiotic"
#     },
#     "fluoxetine": {
#       "quantity": 160,
#       "unit": "capsules",
#       "strength": "20mg",
#       "category": "antidepressant"
#     },
#     "meloxicam": {
#       "quantity": 120,
#       "unit": "tablets",
#       "strength": "15mg",
#       "category": "nsaid"
#     },
#     "methylprednisolone": {
#       "quantity": 100,
#       "unit": "tablets",
#       "strength": "4mg",
#       "category": "corticosteroid"
#     },
#     "celecoxib": {
#       "quantity": 90,
#       "unit": "capsules",
#       "strength": "200mg",
#       "category": "nsaid"
#     },
#     "cetirizine": {
#       "quantity": 180,
#       "unit": "tablets",
#       "strength": "10mg",
#       "category": "antihistamine"
#     },
#     "fexofenadine": {
#       "quantity": 150,
#       "unit": "tablets",
#       "strength": "180mg",
#       "category": "antihistamine"
#     },
#     "propranolol": {
#       "quantity": 140,
#       "unit": "tablets",
#       "strength": "40mg",
#       "category": "beta_blocker"
#     },
#     "valsartan": {
#       "quantity": 160,
#       "unit": "tablets",
#       "strength": "80mg",
#       "category": "blood_pressure"
#     },
#     "trazodone": {
#       "quantity": 120,
#       "unit": "tablets",
#       "strength": "50mg",
#       "category": "antidepressant"
#     },
#     "cyclobenzaprine": {
#       "quantity": 90,
#       "unit": "tablets",
#       "strength": "10mg",
#       "category": "muscle_relaxant"
#     },
#     "baclofen": {
#       "quantity": 100,
#       "unit": "tablets",
#       "strength": "10mg",
#       "category": "muscle_relaxant"
#     },
#     "famotidine": {
#       "quantity": 180,
#       "unit": "tablets",
#       "strength": "20mg",
#       "category": "antacid"
#     },
#     "paroxetine": {
#       "quantity": 140,
#       "unit": "tablets",
#       "strength": "20mg",
#       "category": "antidepressant"
#     },
#     "glipizide": {
#       "quantity": 120,
#       "unit": "tablets",
#       "strength": "5mg",
#       "category": "diabetes"
#     },
#     "hydroxyzine": {
#       "quantity": 100,
#       "unit": "tablets",
#       "strength": "25mg",
#       "category": "antihistamine"
#     },
#     "pravastatin": {
#       "quantity": 150,
#       "unit": "tablets",
#       "strength": "40mg",
#       "category": "statin"
#     },
#     "clonidine": {
#       "quantity": 90,
#       "unit": "tablets",
#       "strength": "0.1mg",
#       "category": "blood_pressure"
#     },
#     "spironolactone": {
#       "quantity": 120,
#       "unit": "tablets",
#       "strength": "25mg",
#       "category": "diuretic"
#     },
#     "dicyclomine": {
#       "quantity": 100,
#       "unit": "capsules",
#       "strength": "10mg",
#       "category": "antispasmodic"
#     },
#     "doxazosin": {
#       "quantity": 90,
#       "unit": "tablets",
#       "strength": "2mg",
#       "category": "blood_pressure"
#     },
#     "nitrofurantoin": {
#       "quantity": 80,
#       "unit": "capsules",
#       "strength": "100mg",
#       "category": "antibiotic"
#     },
#     "ondansetron": {
#       "quantity": 100,
#       "unit": "tablets",
#       "strength": "4mg",
#       "category": "antiemetic"
#     },
#     "promethazine": {
#       "quantity": 90,
#       "unit": "tablets",
#       "strength": "25mg",
#       "category": "antihistamine"
#     },
#     "temazepam": {
#       "quantity": 60,
#       "unit": "capsules",
#       "strength": "15mg",
#       "category": "sedative"
#     },
#     "triamcinolone": {
#       "quantity": 80,
#       "unit": "tubes",
#       "strength": "0.1%",
#       "category": "topical_steroid"
#     },
#     "betamethasone": {
#       "quantity": 70,
#       "unit": "tubes",
#       "strength": "0.05%",
#       "category": "topical_steroid"
#     },
#     "diclofenac": {
#       "quantity": 120,
#       "unit": "tablets",
#       "strength": "75mg",
#       "category": "nsaid"
#     },
#     "oxybutynin": {
#       "quantity": 90,
#       "unit": "tablets",
#       "strength": "5mg",
#       "category": "antispasmodic"
#     },
#     "nifedipine": {
#       "quantity": 100,
#       "unit": "tablets",
#       "strength": "30mg",
#       "category": "calcium_channel_blocker"
#     },
#     "diltiazem": {
#       "quantity": 120,
#       "unit": "tablets",
#       "strength": "120mg",
#       "category": "calcium_channel_blocker"
#     },
#     "tamsulosin": {
#       "quantity": 90,
#       "unit": "capsules",
#       "strength": "0.4mg",
#       "category": "alpha_blocker"
#     },
#     "finasteride": {
#       "quantity": 100,
#       "unit": "tablets",
#       "strength": "5mg",
#       "category": "5_alpha_reductase_inhibitor"
#     },
#     "mirtazapine": {
#       "quantity": 80,
#       "unit": "tablets",
#       "strength": "15mg",
#       "category": "antidepressant"
#     },
#     "pregabalin": {
#       "quantity": 90,
#       "unit": "capsules",
#       "strength": "75mg",
#       "category": "anticonvulsant"
#     },
#     "bupropion": {
#       "quantity": 100,
#       "unit": "tablets",
#       "strength": "150mg",
#       "category": "antidepressant"
#     },
#     "cholecalciferol": {
#       "quantity": 120,
#       "unit": "tablets",
#       "strength": "2000IU",
#       "category": "vitamin"
#     },
#     "cyanocobalamin": {
#       "quantity": 50,
#       "unit": "vials",
#       "strength": "1000mcg/ml",
#       "category": "vitamin"
#     },
#     "iron_sulfate": {
#       "quantity": 180,
#       "unit": "tablets",
#       "strength": "325mg",
#       "category": "mineral_supplement"
#     },
#     "potassium_chloride": {
#       "quantity": 100,
#       "unit": "tablets",
#       "strength": "20mEq",
#       "category": "mineral_supplement"
#     }
#   }
# }
#     main(inventory=db["inventory"],
#          user_input="I have a pain in my lungs.")
        