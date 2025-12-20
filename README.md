
# Fully Free Business Card Data Extractor

Automates the extraction of structured employee and company data from business card images in Google Drive to Google Sheets using the Gemini API.

## Setup

1.  **Clone the repository.**

2.  **Set up a Virtual Environment (Recommended):**
    ```bash
    # Create virtual environment
    python3 -m venv venv
    
    # Activate it (Linux/Mac)
    source venv/bin/activate
    # Activate it (Windows)
    # venv\Scripts\activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
## Configuration & Setup

### 1. Gemini API Key
1.  Go to [Google AI Studio](https://aistudio.google.com/app/apikey).
2.  Click **Create API key**.
3.  Select a project or create a new one.
4.  Copy the generated key string.
5.  Paste it into your `.env` file as `GEMINI_API_KEY`.

### 2. Google Service Account & Drive API
1.  Go to the [Google Cloud Console](https://console.cloud.google.com/).
2.  Create a new project (e.g., "Business Card Extractor").
3.  Enable APIs:
    *   Search for "Google Drive API" -> Enable.
    *   Search for "Google Sheets API" -> Enable.
4.  Create Service Account:
    *   Go to **IAM & Admin** > **Service Accounts**.
    *   Click **Create Service Account**.
    *   Name it (e.g., "card-extractor").
    *   Grant it the **Editor** role (optional but recommended for strictly testing, usually Drive Read-only + Sheets Editor is enough, but 'Editor' covers all).
    *   Click **Done**.
5.  Create Key:
    *   Click on the newly created Service Account (email address).
    *   Go to the **Keys** tab.
    *   Click **Add Key** > **Create new key** > **JSON**.
    *   Save the downloaded JSON file to this project folder (e.g., as `service_account.json`).
6.  Update `.env`:
    *   Set `SERVICE_ACCOUNT_FILE=service_account.json` (or your filename).

### 3. Google Drive Setup
1.  Create a folder on Google Drive.
2.  Upload your business card images (.jpg, .png) to this folder.
3.  **Share the folder**:
    *   Right-click the folder > Share.
    *   Copy the **Client Email** from your Service Account (found in the JSON file or Cloud Console).
    *   Paste it in the Share dialog and send.
4.  Get Folder ID:
    *   Open the folder in your browser.
    *   The URL will look like `drive.google.com/drive/folders/123xyz...`.
    *   Copy the random string (`123xyz...`).
    *   Paste it into `.env` as `DRIVE_FOLDER_ID`.

### 4. Google Sheet Setup
1.  Create a new Google Sheet.
2.  Name it "Business Card Data Extractor" (or whatever matches your config).
3.  **Share the Sheet**:
    *   Click **Share**.
    *   Add the Service Account email (same as for Drive).
    *   Grant **Editor** permission.
4.  Update `.env`:
    *   Set `SHEET_TITLE="Business Card Data Extractor"`.

## Running

```bash
python main.py
```
