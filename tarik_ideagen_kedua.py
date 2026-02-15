import re
import os
from playwright.sync_api import Playwright, sync_playwright, expect
from datetime import datetime
import os

# 1. Ambil waktu sekarang
sekarang = datetime.now()

ideagen_user = os.getenv('IDEAGEN_ID')
ideagen_pass = os.getenv('IDEAGEN_PW')

# 2. Format tanggal sesuai keinginan (DDMMYY -> 090226)
# %d = Day, %m = Month, %y = Year (2 digit)
tgl_str = sekarang.strftime("%d%m%y")

def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://lionairgroup.gaelenlighten.com")

         # 2. Isi username & password
    page.fill("#username", ideagen_user)
    page.fill("#password", ideagen_pass)
    page.wait_for_timeout(1000)
    # 3. Klik tombol login
    page.get_by_role("button", name="Login").click()
    page.wait_for_timeout(10000)
    
    # 2. Buka panel notifikasi
    page.locator("#notifcation-trigger").click()

    # --- BAGIAN KRUSIAL: MENUNGGU TOMBOL MUNCUL ---
    
    # Kita definisikan dulu locator-nya
    download_link = page.get_by_role("link", name=f"risqi_{tgl_str}.csv").first
    
    print("File sudah tersedia, Menunggu file CSV siap di-download...")
    # Tunggu sampai link CSV muncul di dalam panel (timeout 60 detik)
    download_link.wait_for(state="visible", timeout=60000)
    
    # 3. Proses Download
    with page.expect_download() as download_info:
        # Jika klik link tersebut membuka tab baru (popup)
        with page.expect_popup() as page1_info:
            download_link.click()
        page1 = page1_info.value
        
    # Ambil data download
    download = download_info.value
    
    # Menunggu proses download selesai di background
    file_path = download.path() 

    # Tentukan nama folder tujuan
    folder_tujuan = "database"

    # Buat folder jika belum ada
    if not os.path.exists(folder_tujuan):
        os.makedirs(folder_tujuan)
        print(f"Folder '{folder_tujuan}' berhasil dibuat.")

    # Gabungkan nama folder dengan nama file asli
    path_simpan = os.path.join(folder_tujuan, download.suggested_filename)
    
    # Simpan file ke lokasi baru
    download.save_as(path_simpan)
    print(f"File berhasil dipindahkan ke: {path_simpan}")
    # --- MODIFIKASI SELESAI ---
    print(f"Download selesai! File tersimpan di: {file_path}")
    
    # Simpan file ke folder project dengan nama asli
    download.save_as(download.suggested_filename)
    print(f"File disimpan sebagai: {download.suggested_filename}")

    # Cleanup
    page1.close()
    context.close()
    browser.close()

with sync_playwright() as playwright:
    run(playwright)
