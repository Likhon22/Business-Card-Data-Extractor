import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
from src.config import Config

SCOPES = [
    'https://www.googleapis.com/auth/drive.readonly',
    'https://www.googleapis.com/auth/spreadsheets'
]

def get_service_account_creds():
    """Authenticates using the Service Account file."""
    try:
        creds = service_account.Credentials.from_service_account_file(
            Config.SERVICE_ACCOUNT_FILE, scopes=SCOPES
        )
        return creds
    except Exception as e:
        print(f"Error loading service account credentials: {e}")
        raise

def get_drive_service():
    """Returns an authenticated Google Drive service instance."""
    creds = get_service_account_creds()
    return build('drive', 'v3', credentials=creds)

def get_sheets_service():
    """Returns an authenticated Google Sheets service instance."""
    # We will use gspread for easier interaction, but this is good to have for advanced usage if needed.
    # For this project, gspread handles auth internally via credentials object, 
    # so we might just expose the credentials for gspread to use.
    creds = get_service_account_creds()
    return build('sheets', 'v4', credentials=creds)
