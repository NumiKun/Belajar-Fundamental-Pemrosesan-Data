import pandas as pd
from sqlalchemy import create_engine
import gspread
from oauth2client.service_account import ServiceAccountCredentials

def load_data_to_postgresql(df, db_url='postgresql://surya:surya2003@localhost:5432/submissiondb', table_name='products'):
    try:
        engine = create_engine(db_url)
        
        df.to_sql(table_name, engine, if_exists='replace', index=False)
        print("Data berhasil disimpan ke PostgreSQL.")
    except Exception as e:
        print(f"Gagal menyimpan data ke PostgreSQL: {e}")
    finally:
        engine.dispose()

def load_data_to_google_sheets(df, spreadsheet_id='1xTuV-oBslKY0l83Ua0xgDLt3zMm92SnKzxHJ9QalcEU', sheet_name='Sheet1'):
    try:
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        
        creds = ServiceAccountCredentials.from_json_keyfile_name('google-sheets-api.json', scope)
        client = gspread.authorize(creds)

        spreadsheet = client.open_by_key(spreadsheet_id)
        sheet = spreadsheet.worksheet(sheet_name)
        
        sheet.clear()

        sheet.update([df.columns.values.tolist()] + df.values.tolist())
        
        print(f"Data berhasil disimpan ke Google Sheets: {spreadsheet_id} - {sheet_name}")
    
    except gspread.exceptions.APIError as e:
        print(f"Gagal menyimpan data ke Google Sheets: {e}")
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")

def save_to_postgresql_and_sheets(df, db_url='postgresql://surya:surya2003@localhost:5432/submissiondb', spreadsheet_name='1xTuV-oBslKY0l83Ua0xgDLt3zMm92SnKzxHJ9QalcEU', sheet_name='Sheet1'):
    load_data_to_postgresql(df, db_url)
    
    load_data_to_google_sheets(df, spreadsheet_name, sheet_name)
