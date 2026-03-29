import pandas as pd
import gspread
import os
import json # <--- TAMBAHKAN INI
from datetime import datetime

# 1. Konfigurasi
sekarang = datetime.now()
tgl_str = sekarang.strftime("%d%m%y")
folder_db = "database"
nama_file_cleaned = f"cleaned_risqi_{tgl_str}.csv"
path_input = os.path.join(folder_db, nama_file_cleaned)
spreadsheet_id = "1-qmvFshzR9bp0sGv_wXGVcj_KqsIa5dKc2W-nR92HUY"

def sync_to_sheets():
    try:
        if not os.path.exists(path_input):
            print(f"Error: File {path_input} tidak ditemukan!")
            return

        print(f"[{datetime.now().strftime('%H:%M:%S')}] Memproses upload...")

        # --- BAGIAN PERUBAHAN CREDENTIALS ---
        # 1. Ambil teks JSON dari Secret GitHub
        google_json_teks = os.getenv('GSPREAD_JSON')
        
        # 2. Ubah teks string menjadi dictionary
        google_info = json.loads(google_json_teks)
        
        # 3. Auth menggunakan dictionary (bukan file .json)
        gc = gspread.service_account_from_dict(google_info)
        # -------------------------------------

        sh = gc.open_by_key(spreadsheet_id)
        worksheet = sh.worksheet("Jan") 

        df = pd.read_csv(path_input)
        values_only = df[['Details']].values.tolist()

        worksheet.update(range_name='E2', values=values_only)
        print(f"[{datetime.now().strftime('%H:%M:%S')}] SUKSES: Data diisi ke Kolom E mulai baris 2.")

    except Exception as e:
        print(f"Terjadi kesalahan: {e}")

if __name__ == "__main__":
    sync_to_sheets()
