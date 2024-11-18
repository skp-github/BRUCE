from pydantic import BaseModel, Field

class EVENT_ID (BaseModel) :
    event_number : int = Field (..., description="The value of the EVENT_ID key of the event which matches the most")
