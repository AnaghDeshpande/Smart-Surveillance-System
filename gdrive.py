# pip install google-api-python-client watchdog
import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2 import service_account

SCOPES = ['https://www.googleapis.com/auth/drive']
SERVICE_ACCOUNT_FILE = '' # Replace with your Service Account file
PARENT_FOLDER_ID = " "  # Replace with the ID of the parent folder in Google Drive
MONITOR_DIR = 'runs/detect/'  # Directory to monitor for new folders
WAIT_TIME = 10  # Time in seconds to wait before checking folder contents
new_folders = []  # List to store newly detected folders


def authenticate():
    """Authenticate using the service account credentials."""
    creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    return creds


def upload_folder_to_drive(folder_path):
    """
    Upload a folder and its contents to Google Drive.
    """
    creds = authenticate()
    service = build('drive', 'v3', credentials=creds)

    # Create a folder in Google Drive
    folder_name = os.path.basename(folder_path)
    file_metadata = {
        'name': folder_name,
        'mimeType': 'application/vnd.google-apps.folder',
        'parents': [PARENT_FOLDER_ID]
    }
    folder = service.files().create(body=file_metadata, fields='id').execute()
    drive_folder_id = folder.get('id')
    print(f"Created folder '{folder_name}' on Google Drive with ID: {drive_folder_id}")

    # Upload files in the folder
    for root, _, files in os.walk(folder_path):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            file_metadata = {
                'name': file_name,
                'parents': [drive_folder_id]
            }
            media = MediaFileUpload(file_path, resumable=True)
            service.files().create(body=file_metadata, media_body=media, fields='id').execute()
            print(f"Uploaded file '{file_name}' from folder '{folder_name}' to Google Drive")


def upload_detected_folders():
    """
    Upload all newly detected folders to Google Drive.
    """
    global new_folders
    for folder_path in list(new_folders):  # Make a copy to iterate safely
        if os.listdir(folder_path):  # Check if the folder contains any files
            print(f"Uploading folder: {folder_path}")
            upload_folder_to_drive(folder_path)
        else:
            print(f"Folder is empty: {folder_path}. Skipping upload.")
        new_folders.remove(folder_path)  # Remove folder from the list after processing


class FolderCreationHandler(FileSystemEventHandler):
    """
    Event handler for monitoring folder creation in a directory.
    """
    def on_created(self, event):
        if event.is_directory:  # Check if a new folder is created
            print(f"New folder detected: {event.src_path}")
            time.sleep(WAIT_TIME)  # Wait for some time to ensure files are added
            new_folders.append(event.src_path)  # Add the folder to the list


def monitor_directory(directory):
    """
    Monitor a directory for new folders.
    """
    event_handler = FolderCreationHandler()
    observer = Observer()
    observer.schedule(event_handler, directory, recursive=False)
    observer.start()
    print(f"Monitoring directory: {directory}")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


if __name__ == '__main__':
    if not os.path.exists(MONITOR_DIR):
        print(f"Directory '{MONITOR_DIR}' does not exist.")
    else:
        # Start monitoring in a background thread
        import threading

        monitor_thread = threading.Thread(target=monitor_directory, args=(MONITOR_DIR,))
        monitor_thread.daemon = True
        monitor_thread.start()

        print("Monitoring started. You can call `upload_detected_folders()` to upload manually.")
        while True:
            user_input = input("Enter 'upload' to upload detected folders or 'exit' to quit: ").strip().lower()
            if user_input == "upload":
                upload_detected_folders()
            elif user_input == "exit":
                break
