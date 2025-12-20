import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    SERVICE_ACCOUNT_FILE = os.getenv("SERVICE_ACCOUNT_FILE")
    DRIVE_FOLDER_ID = os.getenv("DRIVE_FOLDER_ID")
    SHEET_TITLE = os.getenv("SHEET_TITLE", "Business Card Data Extractor")

    @staticmethod
    def validate():
        missing = []
        if not Config.GEMINI_API_KEY:
            missing.append("GEMINI_API_KEY")
        if not Config.SERVICE_ACCOUNT_FILE:
            missing.append("SERVICE_ACCOUNT_FILE")
        if not Config.DRIVE_FOLDER_ID:
            missing.append("DRIVE_FOLDER_ID")
        
        if missing:
            raise ValueError(f"Missing configuration variables: {', '.join(missing)}")

        if not os.path.exists(Config.SERVICE_ACCOUNT_FILE):
             raise FileNotFoundError(f"Service account file not found at: {Config.SERVICE_ACCOUNT_FILE}")
