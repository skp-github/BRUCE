from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from typing import Optional, List, Literal
from pydantic import BaseModel, Field
import base64
from dotenv import load_dotenv
load_dotenv()

class Item(BaseModel):
    name: str
    quantity: Optional[float]
    price_per_unit: Optional[float]
    total_price: Optional[float]
    unit:Literal["g", "ml", "others"]


class ReceiptSummary(BaseModel):
    store_name: str
    store_address: str
    store_number: Optional[int]
    items: List[Item]
    tax: Optional[float]
    total: Optional[float]
    date: Optional[str] = Field(pattern=r'\d{4}-\d{2}-\d{2}', description="Date in the format YYYY-MM-DD")
    payment_method: Literal["cash", "credit", "debit", "check", "other"]


def encode_image_to_base64(image_path: str) -> str:
    """Convert an image file to base64 string."""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


def process_receipt(image_path: str) -> ReceiptSummary:
    """
    Process a receipt image and extract information according to the schema.

    Args:
        image_path: Path to the receipt image file
        openai_api_key: OpenAI API key

    Returns:
        ReceiptSummary object containing the extracted information
    """

    # Encode the image
    base64_image = encode_image_to_base64(image_path)

    # Initialize the ChatOpenAI model
    chat = ChatOpenAI(
        model="gpt-4o-mini",
        max_tokens=1500,
        temperature=0
    )

    # Create system and human messages
    system_message = SystemMessage(
        content="""You are a receipt processing assistant. Extract information from the receipt image according to the following schema:
        {OUTPUT_SCHEMA}
        Always convert all the quantities in CGS unit
        Provide the output in valid JSON format that matches the schema exactly.""".format(OUTPUT_SCHEMA = ReceiptSummary.model_json_schema())
    )

    human_message = HumanMessage(
        content=[
            {
                "type": "text",
                "text": "Please extract the information from this receipt according to the specified schema."
            },
            {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{base64_image}"
                }
            }
        ]
    )

    # Get response from OpenAI
    chat = chat.with_structured_output(ReceiptSummary)
    response = chat.invoke([system_message, human_message])
    return response


def main():
    # Example usage
    image_path = "IMG_7894.JPG"

    try:
        receipt_summary = process_receipt(image_path)
        print("Receipt processed successfully!")
        print(receipt_summary)
        return receipt_summary.dict()

    except Exception as e:
        print(f"Error processing receipt: {str(e)}")

        return {}


# if __name__ == "__main__":
#     main()