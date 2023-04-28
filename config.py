from google.oauth2 import service_account
from googleapiclient.discovery import build

db_users = 'data/users.db'
tableUsers = 'users'

SCOPES = ['https://www.googleapis.com/auth/drive',
        'https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = 'googlecreds.json'
folder_id = '1qVB0sH_k7uEASpf1MrCCBRnvTGQzMVA-'
table_user_id = '1et-oKQtoUV1XMnc8VzKpBPoN1rU2cX9J0b8qCNItgK8'



credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
drive_service = build('drive', 'v3', credentials=credentials)
sheets_service = build('sheets', 'v4', credentials=credentials)