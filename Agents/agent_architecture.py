import json
from typing import Annotated, TypedDict, List, Dict, Optional, Union, Literal
from pydantic import BaseModel, Field
from langgraph.graph import StateGraph, END, START
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.tools import Tool, StructuredTool
from Tools.meal_planner_tool.main import main as meal_planner
from Tools.medicine_suggestion_tool.main import main as medicine_recommender
from Tools.calender_tool.main import main as calender_oper
from Tools.reciept_extractor.reciept_extractor import main as receipt_extractor
from Agents.llm import initialize_llm
from Agents.sample_data import current_inventory, nutrition_goals, medicine_inventory

from pydantic import BaseModel, field_validator
from datetime import datetime
from typing import Union, Literal
from zoneinfo import ZoneInfo
from tavily import TavilyClient



# class MemoryState(BaseModel):
#     eating_habits: Optional[Dict[str, Union[str, List[str]]]] = Field(default_factory=dict)
#     diet_preferences: Optional[Dict[str, Union[str, List[str]]]] = Field(default_factory=dict)
#     allergies: Optional[List[str]] = Field(default_factory=list)
#     gym_routine: Optional[Dict[str, str]] = Field(default_factory=dict)
#     personal_life: Optional[Dict[str, str]] = Field(default_factory=dict)
#     symptoms: Optional[List[str]] = Field(default_factory=list)
#     medications: Optional[Dict[str, str]] = Field(default_factory=dict)
#     interactions: List[str] = Field(default_factory=list)
#
#     def update_memory(self, category: str, key: str, value: Union[str, List[str]]):
#         """Update memory for a specific category."""
#         if hasattr(self, category):
#             current_field = getattr(self, category)
#             if isinstance(current_field, dict):
#                 current_field[key] = value
#             elif isinstance(current_field, list):
#                 if value not in current_field:
#                     current_field.append(value)
#             setattr(self, category, current_field)
#
#     def retrieve_memory(self, category: str) -> Union[str, List[str], Dict]:
#         """Retrieve memory for a specific category."""
#         return getattr(self, category, {})

# ============= Base Models =============

class InventoryItem(BaseModel):
    quantity: float
    unit: str


class MacroNutrient(BaseModel):
    quantity: float
    unit: str
    calories: int


class NutritionGoals(BaseModel):
    daily_calories: int
    macronutrients: Dict[str, MacroNutrient]


class MealPlannerInput(BaseModel):
    inventory: Dict[str, InventoryItem]
    nutrition: NutritionGoals
    user_input: str

class MedicineRecommendationInput(BaseModel):
    inventory: Dict[str, InventoryItem]
    user_input: str

class EventBody(BaseModel):
    title: str
    description: str
    start_date_time: datetime
    end_date_time: datetime

    @field_validator('start_date_time', 'end_date_time')
    @classmethod
    def validate_timezone(cls, v):
        # Convert to UTC if not already in UTC
        if v.tzinfo is None:
            v = v.replace(tzinfo=ZoneInfo('UTC'))
        return v.astimezone(ZoneInfo('UTC'))

    @field_validator('end_date_time')
    @classmethod
    def validate_end_time(cls, v, info):
        start_time = info.data.get('start_date_time')
        if start_time and v < start_time:
            raise ValueError('end_date_time must be after start_date_time')
        return v


class QueryBody(BaseModel):
    query: str


class DaysBody(BaseModel):
    num_of_days: int

    @field_validator('num_of_days')
    @classmethod
    def validate_days(cls, v):
        if v <= 0:
            raise ValueError('num_of_days must be positive')
        return v


class CalendarDataInput(BaseModel):
    tags: Literal[1, 2, 3]
    body: Union[EventBody, QueryBody, DaysBody]

    @field_validator('body', mode='before')
    @classmethod
    def validate_body_type(cls, v, info):
        if 'tags' not in info.data:
            raise ValueError('tags is required')

        tags = info.data['tags']
        if tags == 1:
            if not all(key in v for key in ['title', 'description', 'start_date_time', 'end_date_time']):
                raise ValueError('Event body must contain title, description, start_date_time, and end_date_time')
            # return EventBody(**v)
        elif tags == 2:
            if 'query' not in v:
                raise ValueError('Query body must contain query')
            # return QueryBody(**v)
        elif tags == 3:
            if 'num_of_days' not in v:
                raise ValueError('Days body must contain num_of_days')
            # return DaysBody(**v)
        return v
# class CalenderData(BaseModel):
#     calender_action: CalendarDataInput

# ============= Agent Response Models =============

class AgentResponse(BaseModel):
    agent_name: str
    decision: str
    confidence: float = Field(ge=0.0, le=1.0)
    reasoning: str
    next_agent: str


class BruceResponse(BaseModel):
    # agent_name: Literal["bruce"] = "bruce"
    confidence: float = Field(ge=0.0, le=1.0)
    decision: Literal["health_query", "resolved"]
    reasoning: str
    next_agent: Literal["david", "ben", "END", "NOT_SUPPORTED", "tyler"]


class DavidResponse(BaseModel):
    agent_name: Literal["david"] = "david"
    confidence: float = Field(ge=0.0, le=1.0)
    decision: Literal["food", "medical", "return"]
    reasoning: str
    next_agent: Literal["gordon", "mike", "RETURN"]

class BenResponse(BaseModel):
    agent_name: Literal["ben"] = "ben"
    confidence: float = Field(ge=0.0, le=1.0)
    decision: Literal["calender", "return"]
    reasoning: str
    next_agent: Literal["bryan", "RETURN"]

class MealPlan(BaseModel):
    meals: Dict[str, List[str]]
    total_calories: int
    macronutrients: Dict[str, float]
    used_ingredients: List[str]


class MedicineRecommendation(BaseModel):
    medicine: Dict[str, List[str]]
    reasoning: str

class GordonResponse(BaseModel):
    agent_name: Literal["gordon"] = "gordon"
    confidence: float = Field(ge=0.0, le=1.0)
    reasoning: str
    next_agent: Literal["david", "REPROCESS"]
    meal_plan: Optional[MealPlan]
    missing_information: Optional[List[str]]

class MikeResponse(BaseModel):
    agent_name: Literal["mike"] = "mike"
    confidence: float = Field(ge=0.0, le=1.0)
    reasoning: str
    next_agent: Literal["david", "REPROCESS"]
    diagnosis : str
    medicine_recommendations: List[str]

class BryanResponse(BaseModel):
    agent_name: Literal["bryan"] = "bryan"
    confidence: float = Field(ge=0.0, le=1.0)
    reasoning: str
    next_agent: Literal["ben", "REPROCESS"]
    tool_input: CalendarDataInput


class AgentState(TypedDict):
    messages: List[BaseMessage]
    next_agent: str
    current_agent: str
    context: dict
    memory: List[str]
    responses: List[Union[BruceResponse, DavidResponse, GordonResponse, MikeResponse, BenResponse, BryanResponse]]


# ============= Tools =============

meal_planning_tool = StructuredTool(
    name="Meal Planner Tool",
    description="Creates personalized meal plans based on dietary needs and preferences",
    func=meal_planner,
    args_schema=MealPlannerInput
)
receipt_extraction_tool = Tool(
    name="Extracts information from receipt",
    description="Extracts items from the receipt to update the inventory",
    func=receipt_extractor
)

medicine_suggestion_tool = StructuredTool(
    name="Medicine Suggestion Tool",
    description="Recommends medicine based on available inventory and symptoms",
    func=medicine_recommender,
    args_schema=MedicineRecommendationInput
)
calendar_operations_tool = StructuredTool(
    name="Calender Operations Tool",
    description="Add, delete and list appointments in the calender",
    func=calender_oper,  #
    args_schema=CalendarDataInput
)
# ============= LLM Initialization =============

llm = initialize_llm()

# ============= Prompts =============

bruce_prompt = ChatPromptTemplate.from_messages([
    ("system", """
You are a helpful personalized assistant for day to day tasks. This is your final persona.
You have a team in order to help you for yours management tasks.
1. Forward to \"david\" who can plan meals for you and suggest you medicines needed. Always ask \"david\" in these situations.
2. Forward to \"ben\" who can help you sort daily tasks and planner. He can access the calendar. Ask him to help you in planning scenarios.
3. In other tasks try to provide help to the person or suggest him a course of action he should take that solves his problem.
4. In case the task is not something you are sure about respond \"NOT_SUPPORTED\".
5. If there is a task to add stuff into inventory and there is a receipt respond \"tyler\".
6. Think in steps : 
    - What was the first query
    - Which agents were called 
    - Do you need to carry on or it's done
    - The agent you are calling, did it already processed the information and sent back to you and you don't need to ask it again and go into loops
    - Pay close attention to the shared states 

Your job is to decide who to call \"david\" or \"ben\" a maximum of once in the entire conversation.
Read the entire conversation available to you and after your team has worked on your problem then it is solved.
In case you have solved the query or someone in your team has given you the solution respond \"END\".
Always be polite and be clear with your help to the personel.
This is some extra personal information from past conversation with the user, use to provide a personalised information:
-{MEMGPT}

"""),
    MessagesPlaceholder(variable_name="messages"),
])

david_prompt = ChatPromptTemplate.from_messages([
    ("system", """
You are a helpful health advisor. You are a part of \"bruce\"\'s team. This is your final persona.
You need to read and understand bruce\'s instruction. You also have a team of experts you can refer to :
1. Direct to \"gordon\" who is an expert chef and can give you a meal plan based on bruce\'s requirements. 
2. Direct to \"mike\" who is world renowned doctor who can prescribe you medicine based on bruce's needs. ALWAYS TRUST MIKE

Your job is to check who has messaged you.
If the last message is bruce then you refer to mike or gordon.
If the last message is mike or gordon then you return their reply to bruce
Respond with \"RETURN\" to go back to bruce with your results.
If mike says he cannot help you, ask bruce.
You NEED to go back to bruce.
"""),
    MessagesPlaceholder(variable_name="messages"),
])



gordon_prompt = ChatPromptTemplate.from_messages([
    ("system", """
You are a world renowned chef and a part of  \"david\"\'s team. This is your final persona.
You have the support of a food tool that will take in ingredients and give you a recipe based on the ingredients available.
The resultant meal plan is here : {GENERATED_MEAL_PLAN}.
Check the meal plan again so that it is similar to what david asked for.
If it is not okay in your opinion then say \"REPROCESS\" in order to generate another meal plan.
Finally say \"RETURN\" to return to david. It is necessary for you to give your solution to david.
"""),
    MessagesPlaceholder(variable_name="messages")
])


mike_prompt = ChatPromptTemplate.from_messages([
    ("system", """
You are a world renowned general physician and you are a part of \"david\"\'s team. This is your final persona.
You have a tool that provides you with a suitable diagnosis from what medicines are available. You are not allowed to provide extra diagnosis on top of that.
Here is the diagnosis suggested by your tool {DIAGNOSIS} and the medications that can be used are : {MEDICATIONS}
You always trust your tools diagnosis to solve david\'s problem.
If you think the diagnosis needs to be changed then direct to \"REPROCESS\" in order to access the tool again.
If you are satisfied with the diagnosis then direct to \"david\" to return to david along with the medications if any.
It is necessary to go back to david

"""
),
    MessagesPlaceholder(variable_name="messages")
])


ben_prompt = ChatPromptTemplate.from_messages([
    ("system", """
You are a Personal Secretary who is a part of \"bruce\"\'s team. You are helpful and polite. This is your final persona.
You need to read and understand bruce\'s instructions. You also have a team of experts to help you with your task :
1. Direct to \"bryan\" when you have any work related to calendars. 
2. Try to provide a solution as to what steps the could be taken in case the problem cannot be solved by your team.

Your job is to understand what bruce needs and direct to your team. 
If you think the query is not solved then direct to \"ben\"(yourself) to do the task again.
Once satisifed then direct to \"bruce\" with the appropriate response.
It is necesaary to go back to bruce.
"""),
    MessagesPlaceholder(variable_name="messages")
])


bryan_gen_prompt = ChatPromptTemplate.from_messages([
("system", """
You are an assistant specialized in understanding and preparing data for calendar operations. 
Your tasks involve determining the type of operation based on specific keywords and constructing the required data structure accordingly:

1. Determine Operation Type:
   - If the request is about *adding* an appointment, set `tags` to 1.
   - If the request involves *deleting* an appointment, set `tags` to 2.
   - If the request involves *listing* appointments, set `tags` to 3.

2. Create the Body Based on `tags` Value:
   - For `tags` = 1 (Add):
     - `body` should be a dictionary with the following four keys:
       - `title`: Information about the appointment.
       - `description`: Additional information about the appointment.
       - `start_date_time`: The appointment start time in UTC ISO format.
       - `end_date_time`: The appointment end time in UTC ISO format.
   - For `tags` = 2 (Delete):
     - `body` should be a dictionary with one key:
       - `query`: A string containing the specific query to identify the appointment to be deleted.
   - For `tags` = 3 (List):
     - `body` should be a dictionary with one key:
       - `num_of_days`: An integer indicating the number of days for which the schedule is requested.
"""),
 MessagesPlaceholder(variable_name="messages")
])

bryan_prompt = ChatPromptTemplate.from_messages([
("system", """
This is the response from the calendar tool: {TOOL_RESPONSE}.
Based on the user query and the response in the `status` key, follow these steps:
   - If you believe the task was completed successfully, report back to "ben".
   - If you want to retry the process, respond with "REPROCESS".
"""),
 MessagesPlaceholder(variable_name="messages")
])



# ============= Response Formatting =============

def format_agent_response(response: AgentResponse) -> str:
    """Format agent responses for message history"""
    if isinstance(response, BruceResponse):
        return f"Bruce's Confidence: {response.confidence:.2f})\nReasoning: {response.reasoning}"

    elif isinstance(response, DavidResponse):
        return f"David's routing decision: {response.next_agent}\nReason for referral: {response.reasoning}\nConfidence: {response.confidence:.2f}"

    elif isinstance(response, GordonResponse):
        if response.meal_plan:
            meals_str = "\n".join([f"{time}: {', '.join(items)}" for time, items in response.meal_plan.meals.items()])
            return f"Meal Planning Results:\n{meals_str}\nTotal Calories: {response.meal_plan.total_calories}\n"
        else:
            missing = ", ".join(response.missing_information or [])
            return f"Need more information: {missing}"

    elif isinstance(response, MikeResponse):
        return f"\n\nDiagnosis : {response.diagnosis} and Medicine Recommendations:\n{response.medicine_recommendations}"

    elif isinstance(response, BenResponse):
        return f"\n\nBen's Response:\n{response}"

    elif isinstance(response, BryanResponse):
        return f"\n\nBryans's Response:\n{response}"



# ============= Agent Functions =============

# def bruce(state: AgentState) -> AgentState:
#     """Initial processing agent with structured response"""
#     # messages = state["messages"]
#     # user_message = messages[0].content
#     # bruce_llm = llm.with_structured_output(BruceResponse)
#     # structured_response = bruce_llm.invoke(bruce_prompt.format(messages=messages))
#     # # state["memory_agent"].process_message(user_message)
#     #
#     # # Retrieve memory for contextual reasoning
#     # # memory_context = state["memory_agent"].get_context()
#     # if structured_response.next_agent == "END":
#     #     # do a llm call for final answer
#     #     pass
#     #
#     # state["next_agent"] = structured_response.next_agent
#     # state["current_agent"] = "bruce"
#     # state["messages"].append(AIMessage(content=format_agent_response(structured_response)))
#     # state.setdefault("responses", []).append(structured_response)
#     #
#     # return state

def generate_final_answer(state: AgentState) -> str:
    """Generate the final answer based on agent responses."""
    combined_responses = "\n".join(
        format_agent_response(response) for response in state["responses"]
    )
    final_prompt = ChatPromptTemplate.from_messages([
        ("system", "Generate the final response based on these inputs:"),
        ("assistant", combined_responses),
        ("user", "Provide a final response.")
    ])
    return llm.invoke(final_prompt.format())

def process_memory_updates(state: AgentState, user_message: str):
    """Extract memory-relevant information from the user input and update memory."""
    memory_update_prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a memory manager. Extract and categorize information from the user's input.
        Categories: eating_habits, diet_preferences, allergies, gym_routine, personal_life, symptoms, medications."""),
        ("user", "{user_message}")
    ])
    memory_response = llm.invoke(memory_update_prompt.format(user_message=user_message))
    state["memory"].append(memory_response.content)
    return

def search_internet(query: str) -> str:
    tavily_client = TavilyClient(api_key="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")
    response = tavily_client.search(query)
    if response and response.get('results'):
        # Extract the most relevant result
        top_result = response['results'][0]
        title = top_result.get('title', 'No title')
        content = top_result.get('content', 'No content available')
        url = top_result.get('url', 'No URL')
        return f"**{title}**\n\n{content}\n\nRead more: {url}"
    else:
        return "No relevant information found."
def bruce(state: AgentState) -> AgentState:
    """Bruce combines agent responses and uses memory for decision-making."""
    messages = state["messages"]
    user_message = messages[0].content

    # Extract relevant information using LLM
    bruce_llm = llm.with_structured_output(BruceResponse)
    structured_response = bruce_llm.invoke(bruce_prompt.format(messages=messages, MEMGPT=state["memory"]))
    # Update memory for contextual reasoning
    process_memory_updates(state, user_message)
    # Handle END to generate the final answer
    if structured_response.next_agent == "END":
        final_answer = generate_final_answer(state)
        state["messages"].append(AIMessage(content=final_answer.content))
        print("Assistant:", final_answer)

    elif structured_response.next_agent == "NOT_SUPPORTED":
        print("Assistant: I currently cannot handle that query with my tools. Would you like me to search the internet? (yes/no)")
        user_decision = input("User: ").strip().lower()
        if user_decision in ["yes", "y"]:
            internet_response = search_internet(user_message)
            state["messages"].append(AIMessage(content=internet_response))
            print("Assistant:", internet_response)
        else:
            print("Assistant: Understood. Let me know if I can assist with anything else.")
        structured_response.next_agent = "END"

    else:
        state["messages"].append(AIMessage(content=format_agent_response(structured_response)))
        state.setdefault("responses", []).append(structured_response)


    # Handle routing
    state["next_agent"] = structured_response.next_agent
    state["current_agent"] = "bruce"



    return state

def tyler(state: AgentState) -> AgentState:
    """Node for extracting receipt data."""
    # messages = state["messages"]
    response_message = receipt_extraction_tool.func()
    state["messages"].append(AIMessage(content=json.dumps(response_message)))
    state["current_agent"] = "tyler"
    state["next_agent"] = "bruce"  # Return control to Bruce after processing

    return state

def david(state: AgentState) -> AgentState:
    """Coordination agent with structured response"""
    messages = state["messages"]
    david_llm = llm.with_structured_output(DavidResponse)

    structured_response = david_llm.invoke(david_prompt.format(messages=messages))

    state["next_agent"] = structured_response.next_agent
    if state["current_agent"] == "mike" :
        state["next_agent"] = "bruce"
    state["current_agent"] = "david"
    state["messages"].append(AIMessage(content=format_agent_response(structured_response)))
    state["responses"].append(structured_response)

    return state

def ben(state: AgentState) -> AgentState:
    """Coordination agent with structured response"""
    messages = state["messages"]
    ben_llm = llm.with_structured_output(BenResponse)

    structured_response = ben_llm.invoke(ben_prompt.format(messages=messages))

    state["next_agent"] = structured_response.next_agent
    state["current_agent"] = "ben"
    state["messages"].append(AIMessage(content=format_agent_response(structured_response)))
    state["responses"].append(structured_response)

    return state

def bryan(state:AgentState) -> AgentState:
    messages = state["messages"]
    bryan_gen_llm = llm.with_structured_output(CalendarDataInput)
    llm_response_input = bryan_gen_llm.invoke(bryan_gen_prompt.format(messages=messages))


    # tool_input = CalenderData(
    #     calendar_action=llm_response_input
    # )
    tool_response = calendar_operations_tool.invoke(llm_response_input.dict())


    # meal_plan = MEAL.validate(tool_response)
    bryan_llm = llm.with_structured_output(BryanResponse)
    structured_response = bryan_llm.invoke(bryan_prompt.format(messages=messages, TOOL_RESPONSE=tool_response))

    state["next_agent"] = structured_response.next_agent
    state["current_agent"] = "bryan"
    state["messages"].append(AIMessage(content=format_agent_response(structured_response)))
    state["responses"].append(structured_response)
    return state



def gordon(state: AgentState) -> AgentState:
    """Meal planning specialist agent with structured response"""
    messages = state["messages"]

    tool_input = MealPlannerInput(
        inventory=current_inventory,
        nutrition=nutrition_goals,
        user_input=messages[0].content
    )
    tool_response = meal_planning_tool.invoke(tool_input.dict())

    # meal_plan = MEAL.validate(tool_response)
    gordon_llm = llm.with_structured_output(GordonResponse)
    structured_response = gordon_llm.invoke(david_prompt.format(messages=messages, GENERATED_MEAL_PLAN=json.loads(tool_response)))

    state["next_agent"] = structured_response.next_agent
    state["current_agent"] = "gordon"
    state["messages"].append(AIMessage(content=format_agent_response(structured_response)))
    state["responses"].append(structured_response)
    return state


def mike(state: AgentState) -> AgentState:
    """Data analysis specialist agent with structured response"""
    messages = state["messages"]
    tool_input = MedicineRecommendationInput(
        inventory=medicine_inventory,
        user_input=messages[0].content
    )
    tool_response = medicine_suggestion_tool.invoke(tool_input.dict())
    mike_llm = llm.with_structured_output(MikeResponse)
    structured_response = mike_llm.invoke(
        mike_prompt.format(messages=messages,DIAGNOSIS=tool_response["Diagnosis"], MEDICATIONS=tool_response["Medication"]))

    state["next_agent"] = structured_response.next_agent
    state["current_agent"] = "mike"
    state["messages"].append(AIMessage(content=format_agent_response(structured_response)))
    state["responses"].append(structured_response)

    return state


# ============= Workflow Functions =============

def should_continue(state: AgentState) -> str:
    """Determine the next node based on agent's decision"""
    next_agent = state["next_agent"]

    if next_agent == "END":
        return END
    elif next_agent == "REPROCESS":
        return state["current_agent"]
    elif next_agent in ["gordon", "mike", "david", "bruce", "ben", "bryan", "tyler"]:
        return next_agent
    else:
        return "bruce"  # Default fallback


def create_workflow() -> StateGraph:
    # """Create and configure the workflow graph"""
    # graph = StateGraph(AgentState)
    #
    # # Add nodes
    # graph.add_node("bruce", bruce)
    # graph.add_node("david", david)
    # graph.add_node("gordon", gordon)
    # graph.add_node("mike", mike)
    #
    # # Add edges
    # graph.add_edge(START, "bruce")
    # graph.add_edge("bruce", "david")
    # graph.add_conditional_edges(
    #     "david",
    #     should_continue,
    #     {
    #         "bruce": "bruce",
    #         "gordon": "gordon",
    #         "mike": "mike",
    #     }
    # )
    # graph.add_edge("gordon", "david")
    # graph.add_edge("mike", "david")
    # graph.add_edge("bruce", END)
    #
    # return graph.compile()

    """Create and configure the workflow graph"""
    graph = StateGraph(AgentState)

    # Add nodes
    graph.add_node("bruce", bruce)
    graph.add_node("david", david)
    graph.add_node("gordon", gordon)
    graph.add_node("mike", mike)
    graph.add_node("ben", ben)
    graph.add_node("bryan", bryan)
    graph.add_node("tyler", tyler)


    # Add edges
    graph.add_edge(START, "bruce")

    # David's routing to specialists
    graph.add_conditional_edges(
        "david",
        should_continue,
        {
            "gordon": "gordon",
            "mike": "mike",
            "bruce": "bruce"
        }
    )
    graph.add_conditional_edges(
        "ben",
        should_continue,
        {
            "bryan": "bryan",
            "bruce": "bruce"
        }
    )

    # Bruce's decision to route or end
    graph.add_conditional_edges(
        "bruce",
        should_continue,
        {
            "david": "david",
            "ben": "ben",
            "tyler": "tyler",
            END: END
        }
    )

    # Gordon and Mike return to David
    graph.add_edge("gordon", "david")
    graph.add_edge("mike", "david")
    graph.add_edge("bryan", "ben")
    graph.add_edge("tyler", "bruce")

    return graph.compile()


def process_query(query: str) -> dict:
    """Process a query through the agent workflow"""
    workflow = create_workflow()

    # initial_state = {
    #     "messages": [HumanMessage(content=query)],
    #     "next_agent": "bruce",
    #     "current_agent": "bruce",
    #     "context": {},
    #     "responses": []
    # }

    try:
        # final_state = workflow.invoke(initial_state)
        for event in workflow.stream({"messages": [HumanMessage(content=query)], "memory":[]}):
            for value in event.values():
                print("Assistant:", value["messages"][-1].content)
        # initial_state = {
        #     "messages": [HumanMessage(content=query)],
        #     "next_agent": "bruce",
        #     "current_agent": "bruce",
        #     "context": {},
        #     "memory": MemoryState(),  # Initialize memory
        #     "responses": []
        # }
        # try:
        #     for event in workflow.stream(initial_state):
        #         for value in event.values():
        #             print("Assistant:", value["messages"][-1].content)
        # except Exception as e:
        #     return {"success": False, "error": str(e), "messages": []}

        # Return structured output
        # return {
        #     "success": True,
        #     "final_agent": final_state["current_agent"],
        #     "responses": [response.dict() for response in final_state["responses"]],
        #     "messages": [msg.content for msg in final_state["messages"]]
        # }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "messages": []
        }


# ============= Main Execution =============

if __name__ == "__main__":
    while True:
        try:
            user_input = input("User: ")
            if user_input.lower() in ["quit", "exit", "q"]:
                print("Goodbye!")
                break

            process_query(user_input)
        except Exception as e:
            # fallback if input() is not available
            user_input = "What do you know about LangGraph?"
            print("User: " + user_input)
            process_query(user_input)
            break