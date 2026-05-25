import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
import os
import sys
import time

# ==========================================
# ⚙️ CONFIGURATION
# ==========================================
JSON_FILE_PATH = os.path.join("Downloads_SRM", "bi_srm_silver_layer.json")
CREDENTIALS_FILE = "credentials.json"

# Actual Spreadsheet URL & GID (Tab ID)
SPREADSHEET_URL = "https://docs.google.com/spreadsheets/d/1eUreKLE1g6hHob4J7Au96evNcXSoqBtz1e38vzqmreQ/edit#gid=1667232139"
TARGET_GID = "1667232139"

# Testing Spreadsheet URL & GID
#SPREADSHEET_URL = "https://docs.google.com/spreadsheets/d/1uQc7p4FgMk0X05QhpszYC0wydnE2HT50nD_Mo35Kno4/edit#gid=1667232139"
#TARGET_GID = "1667232139"

def upload_json_to_sheets(json_path: str, spreadsheet_url: str, credentials_path: str, gid: str) -> None:
    def get_time(): return pd.Timestamp.now().strftime('%H:%M:%S')

    print(f"[{get_time()}] 🚀 Initiating Google Sheets Upload Pipeline...")

    # --- 1. VALIDASI FILE TARGET ---
    if not os.path.exists(json_path):
        print(f"❌ [ERROR] File not found: {json_path}")
        sys.exit(1)

    # --- 2. EKSTRAKSI DATA ---
    print(f"[{get_time()}] 📄 Loading JSON data from {json_path}...")
    try:
        df = pd.read_json(json_path, convert_dates=False)
    except Exception as e:
        print(f"❌ [ERROR] Failed to read JSON: {e}")
        sys.exit(1)

    # --- 3. DATA CLEANSING ---
    print(f"[{get_time()}] 🧹 Sanitizing DataFrame for Google Sheets API...")
    df_clean = df.fillna("").astype(str)
    df_clean = df_clean.replace({"nan": "", "NaT": "", "None": ""})
    
    # --- 4. KONEKSI & AUTENTIKASI API ---
    try:
        print(f"[{get_time()}] 🔐 Authenticating Google Service Account...")
        scopes = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive"
        ]
        creds = Credentials.from_service_account_file(credentials_path, scopes=scopes)
        client = gspread.authorize(creds)
        
        print(f"[{get_time()}] 📡 Connecting to target Spreadsheet...")
        sh = client.open_by_url(spreadsheet_url)
        
        worksheet = next((sheet for sheet in sh.worksheets() if str(sheet.id) == str(gid)), None)
        
        if not worksheet:
            print(f"⚠️ [WARNING] Worksheet GID {gid} missing. Fallback to index 0.")
            worksheet = sh.get_worksheet(0)

        # --- 5. DATA TRANSFORMATION & BATCH UPLOAD ---
        print(f"[{get_time()}] 🔄 Formatting data payload (excluding headers)...")
        # HANYA AMBIL VALUES (mengabaikan nama kolom dari DataFrame agar tidak menimpa baris 1)
        data_to_upload = df_clean.values.tolist()
        
        # Bersihkan sheet HANYA dari baris 2 ke bawah, sampai kolom ZZ (memastikan data lama terhapus)
        print(f"[{get_time()}] 🗑️ Clearing old data from Row 2 downwards in tab '{worksheet.title}'...")
        worksheet.batch_clear(['A2:ZZ'])
        
        # Setting batch upload (10.000 baris per request)
        batch_size = 10000
        total_rows = len(data_to_upload)
        
        print(f"[{get_time()}] 📤 Pushing {total_rows} records in batches of {batch_size}...")
        
        for i in range(0, total_rows, batch_size):
            batch = data_to_upload[i:i + batch_size]
            start_row = i + 2  
            
            print(f"[{get_time()}] ⏳ Uploading rows {start_row}...")
            
            # 1. Tambahkan value_input_option='USER_ENTERED'
            worksheet.update(
                values=batch, 
                range_name=f'A{start_row}', 
                value_input_option='USER_ENTERED'
            )
            
            time.sleep(2)

        # 2. TAMBAHKAN INI: Format otomatis kolom tanggal (Misal kolom B, C, dan J)
        # dd-mmm-yy akan menghasilkan tampilan seperti 10-Apr-26
        print(f"[{get_time()}] 🎨 Applying custom date formatting (dd-mmm-yy)...")
        
        # Contoh: Kolom B (DATE_TIME_OF_EVENT__UTC), C (opened_date_time), dan J (submitted_date_time)
        ranges_to_format = ["B2:B", "C2:C", "J2:J"]
        
        for rng in ranges_to_format:
            worksheet.format(rng, {
                "numberFormat": {
                    "type": "DATE",
                    "pattern": "dd-mmm-yy"
                }
            })
        
        print(f"[{get_time()}] ✅ Pipeline Success! Data is now live on Google Sheets.")
        
    except Exception as e:
        print(f"❌ [ERROR] Upload failed due to API/Connection error: {e}")

# ==========================================
# 🚀 MAIN EXECUTION
# ==========================================
if __name__ == "__main__":
    upload_json_to_sheets(JSON_FILE_PATH, SPREADSHEET_URL, CREDENTIALS_FILE, TARGET_GID)