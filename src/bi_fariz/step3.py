import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
import os
import sys
import time
import json

# ==========================================
# ⚙️ CONFIGURATION
# ==========================================
JSON_FILE_PATH = os.path.join("Downloads_SRM", "bi_fariz_silver_layer.csv")
SPREADSHEET_URL = "https://docs.google.com/spreadsheets/d/1qD_AIJ5yuLfZ4u2yb3LhiuW08PsFQ4sY-83Y8wDn_ow/edit#gid=2011887642"
TARGET_GID = "2011887642"

def upload_json_to_sheets(json_path: str, spreadsheet_url: str, gid: str) -> None:
    def get_time(): return pd.Timestamp.now().strftime('%H:%M:%S')

    print(f"[{get_time()}] 🚀 Initiating Google Sheets Upload Pipeline...")

    # --- 1. VALIDASI FILE TARGET ---
    if not os.path.exists(json_path):
        print(f"❌ [ERROR] File not found: {json_path}")
        sys.exit(1)

    # --- 2. EKSTRAKSI DATA ---
    print(f"[{get_time()}] 📄 Loading JSON data from {json_path}...")
    try:
        df = pd.read_csv(json_path, dtype=str)
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
        google_json_dict = json.loads(os.getenv('GSPREAD_JSON'))
        creds = Credentials.from_service_account_info(google_json_dict, scopes=scopes)
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
            # UPDATE: Mulai dari baris ke-2 (A2, lalu misal A10002, A20002, dst)
            start_row = i + 2  
            end_row = start_row + len(batch) - 1
            
            print(f"[{get_time()}] ⏳ Uploading rows {start_row} to {end_row}...")
            
            # Update hanya di range cell yang spesifik
            worksheet.update(values=batch, range_name=f'A{start_row}')
            
            # Beri jeda 2 detik agar tidak kena blokir Rate Limit API Google (60 requests/minute)
            time.sleep(2)
        
        print(f"[{get_time()}] ✅ Pipeline Success! Data is now live on Google Sheets.")
        
    except Exception as e:
        print(f"❌ [ERROR] Upload failed due to API/Connection error: {e}")

# ==========================================
# 🚀 MAIN EXECUTION
# ==========================================
if __name__ == "__main__":
    upload_json_to_sheets(JSON_FILE_PATH, SPREADSHEET_URL, TARGET_GID)