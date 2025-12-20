import time
from src.config import Config
from src.drive import DriveManager
from src.gemini import GeminiExtractor
from src.sheets import SheetManager, HEADER

def main():
    print("Starting Business Card Data Extractor...")
    
    # 1. Validate Config
    try:
        Config.validate()
        print("Configuration validated.")
    except Exception as e:
        print(f"Startup Error: {e}")
        return

    # 2. Initialize Services
    try:
        drive = DriveManager()
        gemini = GeminiExtractor()
        sheet_manager = SheetManager()
        print("All services initialized successfully.")
    except Exception as e:
        print(f"Initialization Error: {e}")
        return

    # 3. List Images
    images = drive.list_images()
    if not images:
        print("No images found in the specified folder.")
        return

    # 4. Process Loop
    processed_count = 0
    
    print("\n--- Starting Processing Loop ---\n")
    
    # Note: efficient checking if already in sheet could happen here,
    # but requirement implies processing. A simple optimization would be checking existing sheet filenames.
    # For now, we process all found images as requested.
    
    for img in images:
        file_id = img['id']
        file_name = img['name']
        
        print(f"Processing: {file_name}...")
        
        try:
            # Download
            image_bytes = drive.download_image(file_id, file_name)
            
            # Extract
            data = gemini.extract_data(image_bytes, file_name)
            
            if data:
                # Prepare row: HEADER order
                # "fileName", "fullName", "jobTitle", "companyName", "primaryEmail", ...
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
                
                # Append to Sheet
                sheet_manager.append_row(row)
                processed_count += 1
                
                # Rate Limit Safety: Optional sleep if needed, 
                # but Gemini Flash Lite has high RPD. 
                # Flash Lite: 15 RPM, 1 million TPM.
                # A small sleep is good practice.
                time.sleep(2) 
            
        except ResourceWarning:
            print("!!! Quota Exceeded. Safely stopping operation. !!!")
            break
        except Exception as e:
            print(f"Unexpected error on {file_name}: {e}")
            continue

    print(f"\nCompleted. Processed {processed_count}/{len(images)} images.")

if __name__ == "__main__":
    main()
