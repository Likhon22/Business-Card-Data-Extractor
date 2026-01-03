import streamlit as st
import json
import time
import pandas as pd
import gspread
from google import genai
from src.auth import get_service_account_creds, SCOPES
from src.local import list_local_images, read_local_image
from src.gemini import GeminiExtractor
from src.sheets import HEADER
from src.config import Config
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
import io

st.set_page_config(
    page_title="Business Card Extractor",
    page_icon="💼",
    layout="wide"
)

# --- Custom CSS ---
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 1rem;
    }
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="main-header">💼 Business Card Data Extractor</h1>',
            unsafe_allow_html=True)
st.markdown("Extract structured data from business card images using Gemini AI",
            unsafe_allow_html=True)

# --- Sidebar Configuration ---
with st.sidebar:
    st.header("⚙️ Configuration")

    # Gemini API Key
    gemini_key = st.text_input(
        "Gemini API Key",
        type="password",
        value=Config.GEMINI_API_KEY or "",
        help="Get from aistudio.google.com/app/apikey"
    )

    st.divider()

    # Source Selection
    st.subheader("📁 Image Source")
    source_mode = st.radio(
        "Select source:",
        ["Google Drive", "Local Folder"],
        horizontal=True
    )

    if source_mode == "Google Drive":
        st.info("📤 Output: Google Sheets")

        # Service Account Upload
        st.subheader("Google Service Account")
        uploaded_sa = st.file_uploader(
            "Upload JSON (optional)",
            type="json",
            help="If not provided, uses backend default"
        )

        # Sheet Title
        sheet_title = st.text_input(
            "Google Sheet Title",
            value=Config.SHEET_TITLE or "Business Card Data Extractor"
        )

        drive_folder_id = st.text_input(
            "Drive Folder ID",
            value=Config.DRIVE_FOLDER_ID or "",
            help="The ID from your folder URL"
        )
        local_folder_path = None
    else:
        st.info("📥 Output: Downloadable CSV")
        local_folder_path = st.text_input(
            "Local Folder Path",
            placeholder="/home/user/cards/",
            help="Absolute path to folder with images"
        )
        drive_folder_id = None
        uploaded_sa = None
        sheet_title = None

# --- Main Content ---
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📊 Extraction Progress")
    progress_container = st.empty()
    log_container = st.empty()

with col2:
    st.subheader("📈 Stats")
    stats_container = st.empty()

# Download placeholder
download_container = st.empty()

# --- Start Button ---
if st.button("🚀 Start Extraction", type="primary", use_container_width=True):

    # Validation
    if not gemini_key:
        st.error("Please provide a Gemini API Key")
        st.stop()

    if source_mode == "Google Drive" and not drive_folder_id:
        st.error("Please provide a Drive Folder ID")
        st.stop()

    if source_mode == "Local Folder" and not local_folder_path:
        st.error("Please provide a Local Folder Path")
        st.stop()

    try:
        # Initialize Gemini with user-provided API key
        gemini = GeminiExtractor(api_key=gemini_key)

        # Storage for extracted data (used for Local mode CSV)
        extracted_rows = []

        # --- DRIVE MODE: Use Google Sheets ---
        if source_mode == "Google Drive":
            # Parse Service Account
            credentials_dict = None
            if uploaded_sa:
                credentials_dict = json.load(uploaded_sa)

            creds = get_service_account_creds(credentials_dict)

            # Initialize Sheet
            client = gspread.authorize(creds)
            sheet = client.open(sheet_title).sheet1

            # Ensure headers
            first_row = sheet.row_values(1)
            if first_row != HEADER:
                sheet.insert_row(HEADER, 1)

            # Get images from Drive
            drive_service = build('drive', 'v3', credentials=creds)
            query = f"'{drive_folder_id}' in parents and (mimeType contains 'image/')"
            results = drive_service.files().list(q=query, pageSize=1000,
                                                 fields="files(id, name)").execute()
            images = results.get('files', [])

        # --- LOCAL MODE: Collect for CSV ---
        else:
            images = list_local_images(local_folder_path)

        total = len(images)
        processed = 0
        errors = 0

        progress_bar = progress_container.progress(0, text="Starting...")
        log_area = log_container.empty()
        logs = []

        for i, img in enumerate(images):
            file_name = img['name']
            file_id = img['id']

            try:
                # Download/Read image
                if source_mode == "Google Drive":
                    request = drive_service.files().get_media(fileId=file_id)
                    file_io = io.BytesIO()
                    downloader = MediaIoBaseDownload(file_io, request)
                    done = False
                    while not done:
                        status, done = downloader.next_chunk()
                    image_bytes = file_io.getvalue()
                else:
                    image_bytes = read_local_image(file_id)

                # Extract with Gemini
                data = gemini.extract_data(image_bytes, file_name)

                if data:
                    row = [
                        data.get("fileName", ""),
                        data.get("fullName", ""),
                        data.get("jobTitle", ""),
                        data.get("companyName", ""),
                        data.get("primaryEmail", ""),
                        data.get("contactPhone", ""),
                        data.get("websiteURL", ""),
                        data.get("physicalAddress", "")
                    ]

                    if source_mode == "Google Drive":
                        sheet.append_row(row)
                    else:
                        extracted_rows.append(row)

                    processed += 1
                    logs.append(f"✅ {file_name}")
                else:
                    errors += 1
                    logs.append(f"⚠️ {file_name} - No data extracted")

                # Rate limit protection
                time.sleep(2)

            except ResourceWarning:
                st.error("Quota exceeded! Stopping to preserve data.")
                break
            except Exception as e:
                errors += 1
                logs.append(f"❌ {file_name}: {str(e)[:50]}")

            # Update UI
            progress = (i + 1) / total
            progress_bar.progress(
                progress, text=f"Processing {i+1}/{total}...")
            log_area.text_area("Log", "\n".join(logs[-10:]), height=200)
            stats_container.metric(
                "Processed", f"{processed}/{total}", delta=f"{errors} errors")

        st.success(f"✅ Completed! Processed {processed}/{total} images.")

        # --- LOCAL MODE: Show Download Button ---
        if source_mode == "Local Folder" and extracted_rows:
            df = pd.DataFrame(extracted_rows, columns=HEADER)
            # Quote ALL fields to prevent commas from breaking columns
            csv = df.to_csv(index=False, quoting=1).encode(
                'utf-8')  # 1 = csv.QUOTE_ALL

            download_container.download_button(
                label="📥 Download CSV",
                data=csv,
                file_name="extracted_business_cards.csv",
                mime="text/csv",
                type="primary",
                use_container_width=True
            )

        st.balloons()

    except Exception as e:
        st.error(f"Error: {e}")
