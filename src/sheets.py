import gspread
from src.auth import get_service_account_creds
from src.config import Config

HEADER = [
    "fileName", "fullName", "jobTitle", "companyName", "primaryEmail", 
    "contactPhone", "websiteURL", "physicalAddress"
]

class SheetManager:
    def __init__(self):
        self.creds = get_service_account_creds()
        self.client = gspread.authorize(self.creds)
        self.sheet = self._get_or_create_sheet()

    def _get_or_create_sheet(self):
        try:
            # Try to open the sheet by title
            sheet = self.client.open(Config.SHEET_TITLE).sheet1
            print(f"Successfully connected to sheet: {Config.SHEET_TITLE}")
            
            # Check if first row matches expected headers
            first_row = sheet.row_values(1)
            if first_row != HEADER:
                print("Headers missing or incorrect. Inserting header row...")
                sheet.insert_row(HEADER, 1)
            
            return sheet
        except gspread.SpreadsheetNotFound:
            print(f"Error: Spreadsheet '{Config.SHEET_TITLE}' not found.")
            print("Please create the sheet and share it with the Service Account email.")
            raise

    def append_row(self, data):
        """
        Appends a single row of data to the sheet.
        data: list of values matching the HEADER order.
        """
        try:
            self.sheet.append_row(data)
            print(f"Appended row for: {data[0]}") # data[0] is fileName
        except Exception as e:
            print(f"Error appending row: {e}")
            raise
