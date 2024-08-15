from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# Path to your service account key file
SERVICE_ACCOUNT_FILE = 'meli.json'

# Scopes for accessing Google Drive
SCOPES = ['https://www.googleapis.com/auth/drive']

credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)

service = build('drive', 'v3', credentials=credentials)

# File to upload
file_metadata = {'name': 'my_uploaded_file.txt'}
media = MediaFileUpload('./requirements.txt', mimetype='text/plain')

# Upload the file
file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()




file_metadata = {'name': 'my_public_file.txt'}
media = MediaFileUpload('my_public_file.txt', mimetype='text/plain')

# Upload the file
file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()

print(f"File ID: {file.get('id')}")

# Set the file's permissions to public
permission = {
    'type': 'anyone',
    'role': 'reader',
}

service.permissions().create(
    fileId=file.get('id'),
    body=permission,
).execute()


print('File ID:', file.get('id'))
