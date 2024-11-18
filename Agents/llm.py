from langchain_openai import ChatOpenAI
def initialize_llm():
    # model = AzureChatOpenAI(
    #         azure_deployment=get_llm_model_name(),
    #         api_version=get_azure_api_version(),
    #         api_key=get_azure_api_key(),
    #         temperature=get_llm_model_temperature()
    #     )
    model = ChatOpenAI(model="gpt-4o", temperature=0)
    return model