import pandas as pd
import os
import json
import re
from datetime import datetime

# 1. Ambil waktu sekarang
sekarang = datetime.now()

# 2. Format tanggal sesuai keinginan (DDMMYY -> 090226)
# %d = Day, %m = Month, %y = Year (2 digit)
tgl_str = sekarang.strftime("%d%m%y")

# 3. Gabungkan ke nama file
folder_db = "database"
nama_file = f"risqi_{tgl_str}.csv"
path_input = os.path.join(folder_db, nama_file)

def extract_code(text):
    if pd.isna(text):
        return text
    # Regex: Mengambil karakter sebelum ":"
    match = re.search(r'^([^:]+)', str(text))
    if match:
        return match.group(1).strip()
    return text

if os.path.exists(path_input):
    print(f"Membaca file spesifik: {path_input}")
    
    # 2. Load Data
    df = pd.read_csv(path_input)

    # 3. Proses Kolom 'Details'
    if 'Details' in df.columns:
        # Ekstraksi kode
        df['Details'] = df['Details'].apply(extract_code)
        
        # --- PERUBAHAN DI SINI ---
        # Kita hanya ambil kolom 'Details' saja
        df_final = df[['Details']]
        
        # 4. Simpan hasil pembersihan (Hanya 1 kolom)
        path_output = os.path.join(folder_db, f"cleaned_{nama_file}")
        
        # index=False supaya nomor baris tidak ikut tersimpan
        df_final.to_csv(path_output, index=False)
        
        print(f"Berhasil! File bersih (Hanya kolom Details) disimpan sebagai: {path_output}")
    else:
        print(f"Error: Kolom 'Details' tidak ditemukan. Kolom yang ada: {df.columns.tolist()}")
else:

    print(f"Error: File {path_input} tidak ditemukan!")
