from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
 
SERVICE_ACCOUNT_FILE = './client_secret.json'
 
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
 
credential = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
 
SPREADSHEET_ID = '1HEL1umgmrSX3GXEn5FgVoWoYqC8V_Nqipp_lDl415SQ'
RANGE_NAME = 'Sheet1!A2:F11'
 
def main():
    try:
        service = build('sheets', 'v4', credentials=credential)
        sheet = service.spreadsheets()
        values = [
            ['Evans', 'Jl.Batik Kumeli, Kota Bandung', 'evansaja@gmail.com', 'Monitor Samsung 4K', '2', '9000000']
        ]
        body = {
            'values': values
        }
 
        result = sheet.values().update(
            spreadsheetId=SPREADSHEET_ID,
            range=RANGE_NAME,
            valueInputOption='RAW',
            body=body
        ).execute()
 
        print("Berhasil menambahkan data!")
    except Exception as e:
         print(f"An error occurred: {e}")
 
if __name__ == '__main__':
    main()