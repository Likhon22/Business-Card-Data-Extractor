import os
import io
from PIL import Image

def list_local_images(folder_path):
    """
    Lists all image files in a local folder.
    Returns a list of dicts: {'id': file_path, 'name': file_name}
    """
    supported_extensions = ('.jpg', '.jpeg', '.png', '.webp')
    images = []
    
    if not os.path.exists(folder_path):
        raise FileNotFoundError(f"Folder not found: {folder_path}")
    
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(supported_extensions):
            images.append({
                'id': os.path.join(folder_path, filename),
                'name': filename
            })
    
    print(f"Found {len(images)} image files in local folder.")
    return images

def read_local_image(file_path):
    """
    Reads an image file from disk as bytes.
    """
    with open(file_path, 'rb') as f:
        return f.read()
