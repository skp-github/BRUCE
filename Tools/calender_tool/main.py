"""
Main entry point for a calender tool. It can read and write information on to a calender.
"""

from .event_manager import EventManager

def main(tags : int, body: dict) -> str :
    calendar = EventManager()
    status =  calendar.perform_action(action=tags,
                            data=body.dict())
    return status

# if __name__ == "__main__" :
#     main(calendar_action={
#         "action" : 1,
#         "query" : "Remove the event that I have tomorrow",
#         "num_days" : 1,
#         "Title" : "Test",
#         "Description" : "Desc",
#         "Start_time" : "2024-11-20 15:05:17.075067+00:00",
#         "End_time" : "2024-11-20 18:05:17.075067+00:00"
#     })