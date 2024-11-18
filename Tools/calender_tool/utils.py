from .local_constants import (
    CREDENTIAL_PATH,
    CALENDAR_EMAIL,
    AZURE_API_KEY, 
    AZURE_ENDPOINT, 
    MODEL_TEMPERATURE, 
    MODEL_NAME,
    AZURE_API_VERSION
)
from .query_template import (
    CALENDAR_PROMPT,
    PERSONA
)
from .schema import EVENT_ID

def get_credential_path() -> str :
    return CREDENTIAL_PATH

def get_calendar_email() -> str :
    return CALENDAR_EMAIL

def get_azure_api_version() -> str :
    return AZURE_API_VERSION

def get_azure_api_key() -> str :
    return AZURE_API_KEY

def get_azure_endpoint() -> str :
    return AZURE_ENDPOINT

def get_llm_model_temperature() -> int : 
    return MODEL_TEMPERATURE

def get_llm_model_name() -> str :
    return MODEL_NAME

def get_system_prompt() -> str :
    return CALENDAR_PROMPT

def get_model_persona() -> str :
    return PERSONA

def get_llm_schema() -> dict :
    return EVENT_ID.model_json_schema()