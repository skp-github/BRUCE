from .local_constants import (
    AZURE_API_KEY, 
    AZURE_ENDPOINT, 
    MODEL_TEMPERATURE, 
    MODEL_NAME,
    AZURE_API_VERSION
    )

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