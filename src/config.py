import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """
    Config class for optional environment variables.
    These are NOT required - users provide credentials via the Streamlit UI.
    This class exists only for backward compatibility.
    """
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    SERVICE_ACCOUNT_FILE = os.getenv("SERVICE_ACCOUNT_FILE")
    DRIVE_FOLDER_ID = os.getenv("DRIVE_FOLDER_ID")
    SHEET_TITLE = os.getenv("SHEET_TITLE", "Business Card Data Extractor")

    @staticmethod
    def validate():
        """
        DEPRECATED: This validation is no longer used.
        Users provide credentials via the Streamlit UI at runtime.
        """
        raise DeprecationWarning(
            "Config.validate() is deprecated. "
            "Users must provide credentials via the Streamlit UI. "
            "Run 'streamlit run app.py' to use the application."
        )
