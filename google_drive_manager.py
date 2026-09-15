"""
Google Drive Manager - Handles uploading and sharing files with Google Drive
"""

import os
import io
import pickle
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload

# Google Drive API Scopes
SCOPES = ['https://www.googleapis.com/auth/drive.file']

class GoogleDriveManager:
    def __init__(self, credentials_file=None, token_file=None):
        """
        Initialize Google Drive Manager

        Args:
            credentials_file: Path to credentials.json. Defaults to the
                GOOGLE_CREDENTIALS_FILE env var, or 'credentials.json'.
            token_file: Path to the cached token.pickle. Defaults to the
                GOOGLE_TOKEN_FILE env var, or 'token.pickle'.
        """
        self.credentials_file = credentials_file or os.environ.get('GOOGLE_CREDENTIALS_FILE', 'credentials.json')
        self.token_file = token_file or os.environ.get('GOOGLE_TOKEN_FILE', 'token.pickle')
        self.service = None
        self.creds = None
        self.authenticate()

    def authenticate(self):
        """
        Authenticate with Google Drive API.

        On a server (no browser available), this can ONLY use a
        pre-generated token.pickle — it will refresh an expired token if it
        has a refresh_token, but it will never attempt the interactive
        run_local_server() browser flow. Generate token.pickle locally first
        (where a browser is available), then upload it to the server as a
        secret file at the path pointed to by GOOGLE_TOKEN_FILE.
        """
        is_headless = os.environ.get('RENDER') or os.environ.get('HEADLESS_SERVER')

        if os.path.exists(self.token_file):
            with open(self.token_file, 'rb') as token:
                self.creds = pickle.load(token)

        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            elif is_headless:
                raise RuntimeError(
                    f"No valid Google Drive token found at '{self.token_file}'. "
                    "Generate token.pickle locally (run this once on your own machine, "
                    "which can open a browser for the OAuth consent screen), then upload "
                    "it to the server as a secret file at this same path."
                )
            else:
                if not os.path.exists(self.credentials_file):
                    raise FileNotFoundError(
                        f"{self.credentials_file} not found. "
                        "See setup instructions in README.md"
                    )
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_file, SCOPES)
                self.creds = flow.run_local_server(port=0)

            with open(self.token_file, 'wb') as token:
                pickle.dump(self.creds, token)

        self.service = build('drive', 'v3', credentials=self.creds)
        print("✅ Authenticated with Google Drive")
    
    def create_offer_letters_folder(self):
        """
        Create or get the 'Offer Letters' folder in Google Drive
        
        Returns:
            Folder ID
        """
        try:
            # Search for existing folder
            results = self.service.files().list(
                q="name='Offer Letters' and mimeType='application/vnd.google-apps.folder' and trashed=false",
                spaces='drive',
                fields='files(id, name)',
                pageSize=1
            ).execute()
            
            files = results.get('files', [])
            
            if files:
                folder_id = files[0]['id']
                print(f"✅ Found existing folder: {folder_id}")
                return folder_id
            else:
                # Create new folder
                file_metadata = {
                    'name': 'Offer Letters',
                    'mimeType': 'application/vnd.google-apps.folder'
                }
                folder = self.service.files().create(
                    body=file_metadata,
                    fields='id'
                ).execute()
                folder_id = folder.get('id')
                print(f"✅ Created new folder: {folder_id}")
                return folder_id
        except Exception as e:
            print(f"❌ Error managing folder: {str(e)}")
            raise
    
    def upload_file(self, file_name, file_content, mime_type='application/pdf', folder_id=None):
        """
        Upload a file to Google Drive
        
        Args:
            file_name: Name of the file
            file_content: File content (bytes)
            mime_type: MIME type of the file
            folder_id: ID of the parent folder (optional)
        
        Returns:
            File ID and shareable link
        """
        try:
            file_metadata = {'name': file_name}
            
            if folder_id:
                file_metadata['parents'] = [folder_id]
            
            # Create file from bytes
            media = MediaIoBaseUpload(
                io.BytesIO(file_content),
                mimetype=mime_type,
                resumable=True
            )
            
            # Upload file
            file = self.service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id, name, webViewLink, webContentLink'
            ).execute()
            
            file_id = file.get('id')
            print(f"✅ File uploaded: {file_name} (ID: {file_id})")
            
            return {
                'file_id': file_id,
                'file_name': file.get('name'),
                'view_link': file.get('webViewLink'),
                'download_link': file.get('webContentLink')
            }
        except Exception as e:
            print(f"❌ Error uploading file: {str(e)}")
            raise
    
    def make_file_public(self, file_id):
        """
        Make a file publicly accessible
        
        Args:
            file_id: ID of the file
        
        Returns:
            Shareable link
        """
        try:
            # Create permission for anyone
            permission = {
                'type': 'anyone',
                'role': 'reader'
            }
            
            self.service.permissions().create(
                fileId=file_id,
                body=permission
            ).execute()
            
            # Get the shareable link
            file = self.service.files().get(
                fileId=file_id,
                fields='webViewLink, webContentLink'
            ).execute()
            
            print(f"✅ File made public: {file_id}")
            
            return {
                'view_link': file.get('webViewLink'),
                'download_link': file.get('webContentLink')
            }
        except Exception as e:
            print(f"❌ Error making file public: {str(e)}")
            raise
    
    def upload_and_share(self, file_name, file_content, folder_id=None):
        """
        Upload file and make it shareable in one call
        
        Args:
            file_name: Name of the file
            file_content: File content (bytes)
            folder_id: ID of the parent folder (optional)
        
        Returns:
            Shareable link information
        """
        # Upload file
        upload_result = self.upload_file(file_name, file_content, folder_id=folder_id)
        
        # Make it public
        share_result = self.make_file_public(upload_result['file_id'])
        
        # Combine results
        return {
            **upload_result,
            **share_result
        }
