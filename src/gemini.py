from google import genai
from google.genai import types
from src.config import Config
import time
import json


class GeminiExtractor:
    def __init__(self, api_key=None):
        # Only initialize client if api_key is provided
        # Otherwise, client must be set manually before calling extract_data
        self.client = genai.Client(api_key=api_key) if api_key else None
        self.model_name = "gemini-2.5-flash-lite"

        self.system_instruction = """
        You are an expert business card data extractor. Extract structured data from business cards.
        
        FIELD DEFINITIONS:
        - fullName: The PRIMARY person's name on the card (the main contact person, NOT the company name)
        - jobTitle: The person's designation/role (e.g., "Founder & CEO", "Managing Director", "Sales Agent")
        - companyName: The COMPANY or BUSINESS name (not the person's name)
        - primaryEmail: The main email address
        - contactPhone: ALL phone numbers, separated by comma
        - websiteURL: Website address if present
        - physicalAddress: Full office/business address
        
        IMPORTANT RULES:
        1. Distinguish between PERSON NAME and COMPANY NAME carefully
        2. Company names often have "Ltd", "Pvt", "Industries", "Traders", "Corp", "LLC" etc.
        3. Combine ALL phone numbers into one field, separated by commas
        4. If a field is not present, use empty string ""
        5. Output ONLY valid JSON, no extra text
        """

        self.schema = {
            "type": "OBJECT",
            "properties": {
                "fullName": {"type": "STRING"},
                "jobTitle": {"type": "STRING"},
                "companyName": {"type": "STRING"},
                "primaryEmail": {"type": "STRING"},
                "contactPhone": {"type": "STRING"},
                "websiteURL": {"type": "STRING"},
                "physicalAddress": {"type": "STRING"}
            },
            "required": ["fullName", "jobTitle", "companyName", "primaryEmail",
                         "contactPhone", "websiteURL", "physicalAddress"]
        }

    def extract_data(self, image_bytes, file_name):
        """
        Extracts data from an image byte stream using Gemini.
        Returns a dictionary with the extracted fields + fileName.
        """
        prompt = "Extract data from this business card."

        # Prepare the parts: text prompt + image bytes
        # Using types.Part.from_bytes based on google-genai SDK
        image_part = types.Part.from_bytes(
            data=image_bytes, mime_type="image/jpeg")
        # Note: We assume JPEG/PNG. The SDK handles basic types.

        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=[image_part, prompt],
                config=types.GenerateContentConfig(
                    system_instruction=self.system_instruction,
                    response_mime_type="application/json",
                    response_schema=self.schema
                )
            )

            # Parse JSON
            try:
                data = json.loads(response.text)
                data["fileName"] = file_name
                return data
            except json.JSONDecodeError:
                print(
                    f"Error decoding JSON for {file_name}. Raw response: {response.text}")
                return None

        except Exception as e:
            # Print full error details for debugging
            error_str = str(e)
            error_type = type(e).__name__
            print(f"[DEBUG] Error Type: {error_type}")
            print(f"[DEBUG] Full Error: {error_str}")

            # Check for rate limit / quota errors
            if "429" in error_str or "RESOURCE_EXHAUSTED" in error_str or "ResourceExhausted" in error_str:
                print(
                    "Quota exceeded (ResourceExhausted). Stopping execution to preserve data.")
                raise ResourceWarning("Quota exceeded")
            else:
                print(f"Error processing {file_name}: {e}")
                return None
