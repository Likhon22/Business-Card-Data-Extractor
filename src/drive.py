from googleapiclient.http import MediaIoBaseDownload
from src.auth import get_drive_service
from src.config import Config
import io

class DriveManager:
    def __init__(self):
        self.service = get_drive_service()
        self.folder_id = Config.DRIVE_FOLDER_ID

    def list_images(self):
        """
        Lists all image files in the configured Drive folder.
        Returns a list of dicts: {'id': file_id, 'name': file_name}
        """
        query = f"'{self.folder_id}' in parents and (mimeType contains 'image/')"
        try:
            results = self.service.files().list(
                q=query,
                pageSize=1000, 
                fields="nextPageToken, files(id, name, mimeType)"
            ).execute()
            items = results.get('files', [])
            print(f"Found {len(items)} image files.")
            return items
        except Exception as e:
            print(f"Error listing files: {e}")
            raise

    def download_image(self, file_id, file_name):
        """
        Downloads an image file as bytes.
        """
        try:
            request = self.service.files().get_media(fileId=file_id)
            file_io = io.BytesIO()
            downloader = MediaIoBaseDownload(file_io, request)
            
            done = False
            while done is False:
                status, done = downloader.next_chunk()
                # print(f"Download {int(status.progress() * 100)}% for {file_name}.")
            
            return file_io.getvalue()
        except Exception as e:
            print(f"Error downloading {file_name}: {e}")
            raise
