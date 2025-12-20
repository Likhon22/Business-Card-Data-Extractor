from google import genai
from google.genai import types
from src.config import Config
import time
import json

class GeminiExtractor:
    def __init__(self):
        self.client = genai.Client(api_key=Config.GEMINI_API_KEY)
        self.model_name = "gemini-2.5-flash-lite"
        
        self.system_instruction = """
        You are an expert business card data extractor. Your task is to extract all key fields from the provided business card image. 
        The output MUST be a single JSON object that strictly adheres to the provided schema. 
        If a field is not present on the card, its value must be an empty string (" "). 
        Do not include any text outside the JSON block.
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
        image_part = types.Part.from_bytes(data=image_bytes, mime_type="image/jpeg") 
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
                print(f"Error decoding JSON for {file_name}. Raw response: {response.text}")
                return None

        except Exception as e:
            # Handle Resource Exhausted (429) specifically if possible, or general errors
            error_str = str(e)
            if "429" in error_str or "ResourceExhausted" in error_str:
                print("Quota exceeded (ResourceExhausted). Stopping execution to preserve data.")
                raise ResourceWarning("Quota exceeded")
            else:
                print(f"Error processing {file_name}: {e}")
                return None
