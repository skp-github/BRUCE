from langchain_openai import AzureChatOpenAI

from .google_calendar import GoogleCalendarManager
from .utils import (
    get_credential_path,
    get_calendar_email,
    get_azure_api_key,
    get_azure_api_version,
    get_llm_model_name,
    get_llm_model_temperature,
    get_system_prompt,
    get_llm_schema,
    get_model_persona
)
from .schema import EVENT_ID

class EventManager () :
    
    def __init__(self):
        self.calendar_api = GoogleCalendarManager(credentials_path=get_credential_path(),
                                                  calendar_id=get_calendar_email())
        auth_status = self.calendar_api.authenticate()
        if auth_status == False :
            raise Exception("Calendar is not authenticated")
        
        self.model = AzureChatOpenAI(
                        azure_deployment=get_llm_model_name(),
                        api_version=get_azure_api_version(),
                        api_key=get_azure_api_key(),
                        temperature=get_llm_model_temperature()
                        )
                
    def perform_action(self, action : int, data: dict) :
        result = "Something Went Wrong. Operation Failed"
        return_list = []
        if action == 1 :

            status = self.calendar_api.add_event(summary=data["title"],
                                        description=data["description"],
                                        start_time=data["start_date_time"],
                                        end_time=data["end_date_time"])
            if status == True :
                result = "Event Added Successfully"
                
        elif action == 2 :
            event_list = self.calendar_api.list_upcoming_events()
            status = self.calendar_api.delete_event(event_id=self.match_event_to_delete(events_list=event_list,
                                             query=data["query"]))
            if status == True :
                result = "Event Removed Successfully"

        else:
            if "num_days" in data :
                event_list = self.calendar_api.list_upcoming_events(num_days=data["num_of_days"])
            else :    
                event_list = self.calendar_api.list_upcoming_events()
            for event in event_list:
                print(f"Event: {event['summary']}, Start: {event['start'].get('dateTime', event['start'].get('date'))}")
            result = "Events Listed Successfully"
            return_list = event_list

        return {"status":result, "event_list": return_list}

        
    def build_prompt (self, events, query) -> list :
        prompt_list = [
            ("system", get_system_prompt().format(EVENTS = events,
                                                  PERSONA = get_model_persona(),
                                                  QUERY = query,
                                                  SCHEMA = get_llm_schema()))
        ]
        return prompt_list
         
    def match_event_to_delete (self, events_list : dict, query : str) -> str :
        refactor_events = []
        for idx, event in enumerate(events_list) :
            event["Event_Number"] = idx
            refactor_events.append(event)
        prompt_list = self.build_prompt(refactor_events, query)
        structured_model = self.model.with_structured_output(EVENT_ID)
        idx = structured_model.invoke(input=prompt_list).event_number
        return events_list[idx]["id"]
    
# # Example usage
# if __name__ == '__main__':
#     # Replace these with your actual values
#     credentials_path = 'calender_tool/credentials.json'
    
#     # Your calendar ID (email address)
#     # This should be YOUR email address, not the service account email
#     calendar_id = 'linkme06@gmail.com'  # Replace with your email
    
#     # Initialize the calendar manager with your calendar ID
#     calendar = GoogleCalendarManager(credentials_path, calendar_id)
    
#     if calendar.authenticate():
#         # # Create an event tomorrow
#         start_time = datetime.now(timezone.utc) + timedelta(days=2)
#         end_time = start_time + timedelta(hours=2)
        
#         new_event = calendar.add_event(
#             summary='Lag gaye laure',
#             description='Do din lagake adha futa feature banaya enam ke best friend ne',
#             start_time=start_time,
#             end_time=end_time,
#             timezone='UTC'
#         )

#         # List upcoming events
#         print("\nListing upcoming events:")
#         events = calendar.list_upcoming_events(max_results=5)
#         for event in events:
#             print(event)
#             print(f"Event: {event['summary']}, Start: {event['start'].get('dateTime', event['start'].get('date'))}")

#         # Delete the test event
#         # if True:
#         #     print("\nDeleting the test event...")
#         #     calendar.delete_event("dTgyMmFrMDBnN25pa2JtaG03ZzYwMzloMGMgbGlua21lMDZAbQ")