from src.auth import get_drive_service, get_sheets_service, get_service_account_creds
from src.config import Config
import gspread

def test_drive():
    try:
        service = get_drive_service()
        # Try to list just 1 item from that folder to verify access
        query = f"'{Config.DRIVE_FOLDER_ID}' in parents"
        results = service.files().list(
            q=query, pageSize=1, fields="files(id, name)"
        ).execute()
        files = results.get('files', [])
        print(f"[SUCCESS] Drive Connected! Found {len(files)} file(s) in folder (listing only 1).")
        if files:
            print(f"   - Visible file: {files[0]['name']}")
        return True
    except Exception as e:
        print(f"[FAIL] Drive Error: {e}")
        return False

def test_sheet():
    try:
        creds = get_service_account_creds()
        client = gspread.authorize(creds)
        
        # Try to open the sheet
        sheet = client.open(Config.SHEET_TITLE).sheet1
        print(f"[SUCCESS] Sheet Connected! Opened '{Config.SHEET_TITLE}'.")
        
        # Check current content size
        values = sheet.get_all_values()
        print(f"   - Current rows: {len(values)}")
        return True
    except Exception as e:
        print(f"[FAIL] Sheet Error: {e}")
        return False

def test_gemini_key():
    # This just checks if the key is loaded, not if it works (to save quota)
    if Config.GEMINI_API_KEY and Config.GEMINI_API_KEY.startswith("AIza"):
        print("[SUCCESS] Gemini API Key is present and looks valid (starts with AIza).")
        return True
    else:
        print("[FAIL] Gemini API Key is missing or invalid format.")
        return False

if __name__ == "__main__":
    print("--- Running Connection Tests (No API Quota Used) ---\n")
    d = test_drive()
    s = test_sheet()
    g = test_gemini_key()
    
    if d and s and g:
        print("\nAll systems green! You are ready to run the main script.")
    else:
        print("\nSome tests failed. Check your credentials and sharing settings.")
