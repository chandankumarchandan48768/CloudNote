from google.oauth2 import service_account
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/drive.file"]

def authenticate_drive():
    creds = service_account.Credentials.from_service_account_file(
        "", scopes=SCOPES
    )
    return build("drive", "v3", credentials=creds)
