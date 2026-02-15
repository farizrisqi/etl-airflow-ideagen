import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import re
from playwright.sync_api import Playwright, sync_playwright, expect


def upload_ke_sheets(file_path):
    # 1. SETUP API (Sama seperti sebelumnya)
    # Ambil teks JSON dari Secret GitHub
    google_json_teks = os.getenv('GSPREAD_JSON')
    google_json_dict = json.loads(google_json_teks)

    # Login pake dictionary (bukan file)
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_dict(google_json_dict, scope)
    client = gspread.authorize(creds)
    
    sheet_id = "1axm9YL2jok_JBd-LDSPbjCrTQISZ9lTU3G8lL74IIMg"
    sheet = client.open_by_key(sheet_id).get_worksheet(0)

    # 2. TRANSFORM
    # Baca excel, skiprows=1 untuk skip baris pertama excel yang mungkin kotor
    df = pd.read_excel(file_path, skiprows=1)
    
    # --- PENTING: Hapus baris yang benar-benar kosong di file sumber ---
    # how='all' artinya hanya hapus jika SATU BARIS itu kosong semua nilainya
    df = df.dropna(how='all') 
    
    # Bersihkan NaN (data kosong) agar tidak error saat kirim ke Google Sheets
    df = df.fillna('')

    # 3. CLEAR (Hapus data lama di Spreadsheet, baris 1 aman)
    # Kita hapus mulai dari baris 2 sampai baris ke-5000 (sesuaikan jika data kamu lebih banyak)
    range_to_clear = 'A2:Z5000'
    sheet.batch_clear([range_to_clear])
    print(f"🧹 Data lama sudah dibersihkan (Header tetap aman).")

    # 4. LOAD (Update/Replace data baru mulai dari baris A2)
    data_list = df.values.tolist()
    
    # Menggunakan update() mulai dari sel A2 agar baris 1 (header) tidak hilang
    sheet.update('A2', data_list)
    
    print(f"🚀 Data baru berhasil masuk ke sheet pada: {datetime.now()}")

def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://ops-report.lionair.com/ops-report/index.php/auth")
    page.locator("#exampleInputID").click()
    page.locator("#exampleInputID").click()
    page.locator("#exampleInputID").fill("fda.csq")
    page.get_by_role("textbox", name="Password").click()
    page.get_by_role("textbox", name="Password").fill("fda.csq")
    page.get_by_role("button", name="Log In").click()
    page.get_by_role("listitem").filter(has_text="Leg Complement").click()
    page.get_by_role("link", name="Leg Complement").click()
    page.get_by_role("button", name="Retrieve").click()
    with page.expect_download() as download_info:
        # Klik tombol yang memicu download
        page.get_by_role("button", name="Excel").click()
    
    # Menunggu proses download selesai dan mengambil objek download
    download = download_info.value

    # --- LANGKAH PENTING: Pindahkan dari folder temp ke folder kerja ---
    nama_file = "data_lion_air.xlsx"
    download.save_as(nama_file) 
    
    print(f"✅ Muatan aman! Tersimpan di folder WSL kamu sebagai: {nama_file}")
    
    # Tutup halaman setelah selesai
    page.close()


    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)

upload_ke_sheets("data_lion_air.xlsx")
