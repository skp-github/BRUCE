"""
This is a meal planner tool. Probably takes in two dictionaries and creates a meal plan.
"""


from .planner import MealPlanner


def main(inventory : dict, nutrition : dict, user_input : str) -> dict :
    """
    Main entry point for the Meal planner tool.
    
    Args :
        inventory (dict) : All the ingredients that are available to the meal planner.
        nutrition (dict) : The nutritional goals for the day
        user_input (dict) : The input prompt of the user
        
    Returns :
        dict : The Meal plan for the day.
    """
    
    try :
        # NOTE: Lazy checking for now, should be changed later
        if inventory == {} :
            raise ValueError("The inventory cannot be empty")
        if nutrition == {} :
            raise ValueError("There needs to be nutritional goals for the day.")
        
        # TODO: Check for proper schema for the inventory and the nutrition
                
        planner = MealPlanner(ingredients=inventory,
                              nutrition=nutrition)
        generated_meal = planner.build_meal(user_input=user_input)
        print(f"KHA LE : {generated_meal}")
        return generated_meal
    except Exception as e:
        raise(e)
        
# if __name__ == "__main__" :
#     db = {
#             "inventory": {
#             "milk": {"quantity": 1000, "unit": "ml"},
#             "eggs": {"quantity": 12, "unit": "number"},
#             "greek_yogurt": {"quantity": 500, "unit": "g"},
#             "cottage_cheese": {"quantity": 250, "unit": "g"},
#             "mozzarella": {"quantity": 200, "unit": "g"},
#             "cheddar_cheese": {"quantity": 200, "unit": "g"},
#             "parmesan": {"quantity": 100, "unit": "g"},
#             "butter": {"quantity": 250, "unit": "g"},
#             "chicken_breast": {"quantity": 1000, "unit": "g"},
#             "salmon": {"quantity": 500, "unit": "g"},
#             "tuna": {"quantity": 400, "unit": "g"},
#             "shrimp": {"quantity": 300, "unit": "g"},
#             "tofu": {"quantity": 400, "unit": "g"},
#             "tempeh": {"quantity": 200, "unit": "g"},
#             "ground_beef": {"quantity": 500, "unit": "g"},
#             "pork_loin": {"quantity": 400, "unit": "g"},
#             "turkey_breast": {"quantity": 500, "unit": "g"},
#             "lamb": {"quantity": 300, "unit": "g"},
#             "brown_rice": {"quantity": 1000, "unit": "g"},
#             "quinoa": {"quantity": 500, "unit": "g"},
#             "oats": {"quantity": 800, "unit": "g"},
#             "barley": {"quantity": 400, "unit": "g"},
#             "whole_wheat_bread": {"quantity": 500, "unit": "g"},
#             "whole_wheat_pasta": {"quantity": 500, "unit": "g"},
#             "couscous": {"quantity": 300, "unit": "g"},
#             "bulgur": {"quantity": 300, "unit": "g"},
#             "spinach": {"quantity": 300, "unit": "g"},
#             "kale": {"quantity": 200, "unit": "g"},
#             "arugula": {"quantity": 150, "unit": "g"},
#             "lettuce": {"quantity": 300, "unit": "g"},
#             "broccoli": {"quantity": 500, "unit": "g"},
#             "cauliflower": {"quantity": 400, "unit": "g"},
#             "carrots": {"quantity": 400, "unit": "g"},
#             "sweet_potatoes": {"quantity": 600, "unit": "g"},
#             "regular_potatoes": {"quantity": 800, "unit": "g"},
#             "bell_peppers": {"quantity": 400, "unit": "g"},
#             "cucumber": {"quantity": 300, "unit": "g"},
#             "tomatoes": {"quantity": 500, "unit": "g"},
#             "zucchini": {"quantity": 400, "unit": "g"},
#             "eggplant": {"quantity": 300, "unit": "g"},
#             "mushrooms": {"quantity": 300, "unit": "g"},
#             "onions": {"quantity": 500, "unit": "g"},
#             "garlic": {"quantity": 200, "unit": "g"},
#             "ginger": {"quantity": 100, "unit": "g"},
#             "celery": {"quantity": 300, "unit": "g"},
#             "asparagus": {"quantity": 250, "unit": "g"},
#             "brussels_sprouts": {"quantity": 300, "unit": "g"},
#             "cabbage": {"quantity": 500, "unit": "g"},
#             "corn": {"quantity": 400, "unit": "g"},
#             "peas": {"quantity": 300, "unit": "g"},
#             "green_beans": {"quantity": 300, "unit": "g"},
#             "beets": {"quantity": 300, "unit": "g"},
#             "apples": {"quantity": 6, "unit": "number"},
#             "bananas": {"quantity": 5, "unit": "number"},
#             "oranges": {"quantity": 4, "unit": "number"},
#             "lemons": {"quantity": 3, "unit": "number"},
#             "limes": {"quantity": 3, "unit": "number"},
#             "strawberries": {"quantity": 300, "unit": "g"},
#             "blueberries": {"quantity": 200, "unit": "g"},
#             "raspberries": {"quantity": 150, "unit": "g"},
#             "blackberries": {"quantity": 150, "unit": "g"},
#             "pineapple": {"quantity": 500, "unit": "g"},
#             "mango": {"quantity": 300, "unit": "g"},
#             "grapes": {"quantity": 400, "unit": "g"},
#             "pears": {"quantity": 4, "unit": "number"},
#             "peaches": {"quantity": 4, "unit": "number"},
#             "plums": {"quantity": 6, "unit": "number"},
#             "avocado": {"quantity": 3, "unit": "number"},
#             "coconut_milk": {"quantity": 400, "unit": "ml"},
#             "almond_milk": {"quantity": 1000, "unit": "ml"},
#             "soy_milk": {"quantity": 1000, "unit": "ml"},
#             "olive_oil": {"quantity": 500, "unit": "ml"},
#             "coconut_oil": {"quantity": 250, "unit": "ml"},
#             "sesame_oil": {"quantity": 200, "unit": "ml"},
#             "almonds": {"quantity": 200, "unit": "g"},
#             "walnuts": {"quantity": 200, "unit": "g"},
#             "cashews": {"quantity": 200, "unit": "g"},
#             "pecans": {"quantity": 150, "unit": "g"},
#             "pistachios": {"quantity": 150, "unit": "g"},
#             "peanuts": {"quantity": 200, "unit": "g"},
#             "chia_seeds": {"quantity": 100, "unit": "g"},
#             "flax_seeds": {"quantity": 100, "unit": "g"},
#             "pumpkin_seeds": {"quantity": 150, "unit": "g"},
#             "sunflower_seeds": {"quantity": 150, "unit": "g"},
#             "protein_powder": {"quantity": 500, "unit": "g"},
#             "chickpeas": {"quantity": 400, "unit": "g"},
#             "black_beans": {"quantity": 400, "unit": "g"},
#             "kidney_beans": {"quantity": 400, "unit": "g"},
#             "lentils": {"quantity": 400, "unit": "g"},
#             "pinto_beans": {"quantity": 400, "unit": "g"},
#             "rice_noodles": {"quantity": 300, "unit": "g"},
#             "soba_noodles": {"quantity": 300, "unit": "g"},
#             "tortillas": {"quantity": 12, "unit": "number"},
#             "pita_bread": {"quantity": 8, "unit": "number"},
#             "maple_syrup": {"quantity": 200, "unit": "ml"},
#             "honey": {"quantity": 250, "unit": "ml"},
#             "dates": {"quantity": 200, "unit": "g"},
#             "raisins": {"quantity": 150, "unit": "g"},
#             "dried_cranberries": {"quantity": 150, "unit": "g"},
#             "cocoa_powder": {"quantity": 200, "unit": "g"},
#             "dark_chocolate": {"quantity": 200, "unit": "g"},
#             "vanilla_extract": {"quantity": 100, "unit": "ml"},
#             "cinnamon": {"quantity": 100, "unit": "g"},
#             "turmeric": {"quantity": 100, "unit": "g"},
#             "cumin": {"quantity": 100, "unit": "g"},
#             "paprika": {"quantity": 100, "unit": "g"},
#             "basil": {"quantity": 50, "unit": "g"},
#             "oregano": {"quantity": 50, "unit": "g"},
#             "thyme": {"quantity": 50, "unit": "g"},
#             "rosemary": {"quantity": 50, "unit": "g"}
#             },
#             "nutrition_goals": {
#             "daily_calories": 2000,
#             "macronutrients": {
#                 "protein": {"quantity": 150, "unit": "g", "calories": 600},
#                 "carbs": {"quantity": 225, "unit": "g", "calories": 900},
#                 "fat": {"quantity": 55, "unit": "g", "calories": 500}
#             },
#             "meal_distribution": {
#                 "breakfast": {"calories": 500},
#                 "lunch": {"calories": 600},
#                 "dinner": {"calories": 700},
#                 "snacks": {"calories": 200}
#             }
#             }
#         }
#     main(inventory=db["inventory"],
#          nutrition=db["nutrition_goals"],
#          user_input="Give me a meal plan for lunch")
        