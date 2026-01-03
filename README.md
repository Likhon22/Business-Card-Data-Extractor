# Business Card Data Extractor

Extract structured employee and company data from business card images using Gemini AI with a friendly web interface.

## Features

- 💼 Extract data from business card images
- 🌐 **Google Drive Mode**: Process images from Google Drive, save to Google Sheets
- 📁 **Local Folder Mode**: Process local images, download results as CSV
- 🖥️ User-friendly Streamlit web interface
- 🔒 Secure: Users provide their own credentials (nothing stored by default)

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

## Running the Application

```bash
streamlit run app.py
```

This will open a web interface in your browser where you can:

- Enter your Gemini API Key
- Choose between Google Drive or Local Folder mode
- Configure your settings
- Click "Start Extraction" to process images

## Configuration

### For Google Drive Mode:

#### 1. Gemini API Key

1.  Go to [Google AI Studio](https://aistudio.google.com/app/apikey).
2.  Click **Create API key**.
3.  Copy the generated key.
4.  Paste it in the web interface when running the app.

#### 2. Google Service Account (for Drive & Sheets)

1.  Go to the [Google Cloud Console](https://console.cloud.google.com/).
2.  Create a new project (e.g., "Business Card Extractor").
3.  Enable APIs:
    - Search for "Google Drive API" -> Enable.
    - Search for "Google Sheets API" -> Enable.
4.  Create Service Account:
    - Go to **IAM & Admin** > **Service Accounts**.
    - Click **Create Service Account**.
    - Name it (e.g., "card-extractor").
    - Grant it appropriate permissions.
    - Click **Done**.
5.  Create Key:
    - Click on the newly created Service Account.
    - Go to the **Keys** tab.
    - Click **Add Key** > **Create new key** > **JSON**.
    - Save the downloaded JSON file.
6.  **Upload the JSON file** in the Streamlit web interface when running the app.

#### 3. Google Drive Setup

1.  Create a folder on Google Drive.
2.  Upload your business card images (.jpg, .png) to this folder.
3.  **Share the folder**:
    - Right-click the folder > Share.
    - Add the Service Account email (from the JSON file).
    - Grant **Editor** permission.
4.  Get Folder ID:
    - Open the folder in your browser.
    - The URL will look like `drive.google.com/drive/folders/123xyz...`.
    - Copy the ID (`123xyz...`).
    - Paste it in the web interface when running the app.

#### 4. Google Sheet Setup

1.  Create a new Google Sheet.
2.  **Share the Sheet**:
    - Click **Share**.
    - Add the Service Account email.
    - Grant **Editor** permission.
3.  Enter the sheet title in the web interface when running the app.

### For Local Folder Mode:

1.  Get your Gemini API Key (same as step 1 above).
2.  Place your business card images in a local folder.
3.  In the web interface:
    - Enter your Gemini API Key
    - Select "Local Folder" mode
    - Enter the absolute path to your folder
    - Click "Start Extraction"
4.  Download the results as a CSV file when processing completes.

## Notes

- No credentials are stored by default - users must provide them each time
- The `.env` file is optional and not required for running the application
- All processing happens when you click the "Start Extraction" button
