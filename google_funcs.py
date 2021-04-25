from google.oauth2 import service_account
from googleapiclient.http import MediaIoBaseDownload,MediaFileUpload
from googleapiclient.discovery import build
import io
from apiclient import errors
import httplib2


SCOPES = ['https://www.googleapis.com/auth/drive',
        'https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = 'googlecreds.json'
folder_id = '1qVB0sH_k7uEASpf1MrCCBRnvTGQzMVA-'
table_ekb_id = '19XM65sKrVOFa33Kwu-9DMTvUbyesR_7jPmRokHUmQNE'
table_spb_id = '1JeJhN3BkqAPf2mnPqtsmGm80GzbQ7VN23i1_elGtS_Y'
table_krd_id = '1UmzxaUNBvBr3bz4zWRWkm4YEZfeinqWzCLYf8_KGkXc'
table_chlb_id = '1AmZStO4CKuc6nCuV_L-254hsiO_xOlb2S8-EES7PnlI'
table_tvr_id = '1wdw0qt7wwv7ZAR_oaNXPBB1DeAsG_FiHIdTp6UNm-aE'
table_test_id = '1et-oKQtoUV1XMnc8VzKpBPoN1rU2cX9J0b8qCNItgK8'
list_name_java = 'Стажер-разработчик Java'
list_name_tester = 'Стажер-тестировщик'
list_name_analytics = 'Стажер-аналитик'
list_name_techwriter = 'Стажер технический писатель'



credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
drive_service = build('drive', 'v3', credentials=credentials)
sheets_service = build('sheets', 'v4', credentials=credentials)


def add_new_trainee(table_id, list_name, values, id_bd):
    _range = list_name + ("!A%s:BB%s" % (str(id_bd+1),str(id_bd+1)))
    body = {"valueInputOption": "USER_ENTERED", # Данные воспринимаются, как вводимые пользователем (считается значение формул)
    "data": [
        {"range": _range,
         "majorDimension": "ROWS",     # Сначала заполнять строки, затем столбцы
         "values": [
                    values
                   ]}
    ]}
    sheets_service.spreadsheets().values().batchUpdate(spreadsheetId=table_id,
                                                        body=body).execute()

def get_forms_list(tg_id):
    pass


