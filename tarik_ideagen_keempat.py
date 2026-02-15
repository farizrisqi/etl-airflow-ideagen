import pandas as pd
import gspread
import os
from datetime import datetime

# 1. Ambil waktu sekarang
sekarang = datetime.now()

# 2. Format tanggal sesuai keinginan (DDMMYY -> 090226)
# %d = Day, %m = Month, %y = Year (2 digit)
tgl_str = sekarang.strftime("%d%m%y")

# 1. Konfigurasi
folder_db = "database"
nama_file_cleaned = f"cleaned_risqi_{tgl_str}.csv"
path_input = os.path.join(folder_db, nama_file_cleaned)
path_key_json = "credentials.json" 
spreadsheet_id = "1-qmvFshzR9bp0sGv_wXGVcj_KqsIa5dKc2W-nR92HUY"

def sync_to_sheets():
    try:
        if not os.path.exists(path_input):
            print(f"Error: File {path_input} tidak ditemukan!")
            return

        print(f"[{datetime.now().strftime('%H:%M:%S')}] Memproses upload ke Kolom E baris 2...")
        # 2. Auth
        gc = gspread.service_account(filename=path_key_json)
        sh = gc.open_by_key(spreadsheet_id)
        worksheet = sh.worksheet("Jan") # Sesuaikan jika sheet tujuannya bukan tab pertama
        # 3. Baca Data (Hanya kolom Details)
        df = pd.read_csv(path_input)
        # Ambil valuenya saja tanpa header (karena mulai dari baris 2)
        # Kita ubah menjadi list of lists untuk gspread
        # Ambil valuenya saja dan pastikan dalam bentuk list of lists
        # .tolist() dari pandas series perlu dibungkus lagi agar terbaca sebagai baris/kolom
        values_only = df[['Details']].values.tolist()
        # 4. Update ke Kolom E Baris 2
        # Menggunakan argumen eksplisit untuk menghindari error index
        worksheet.update(range_name='E2', values=values_only)
        print(f"[{datetime.now().strftime('%H:%M:%S')}] SUKSES: Data diisi ke Kolom E mulai baris 2.")

    except Exception as e:
        print(f"Terjadi kesalahan: {e}")

if __name__ == "__main__":
    sync_to_sheets()