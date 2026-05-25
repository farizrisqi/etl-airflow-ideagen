import re
import os
from datetime import datetime
from playwright.sync_api import Playwright, sync_playwright, expect

def run(playwright: Playwright) -> None:
    # --- KONFIGURASI PATH ---
    # Membuat folder 'Downloads_SRM' di lokasi script ini berada
    download_dir = os.path.join(os.getcwd(), "Downloads_SRM")
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)
    
    print("🚀 Memulai browser Chromium...")
    browser = playwright.chromium.launch(headless=True)
    
    print("📂 Memuat context dengan session storage_state...")
    context = browser.new_context(ignore_https_errors=True, storage_state="state.json")
    context.set_default_timeout(600000)
    context.set_default_navigation_timeout(600000)

    page = context.new_page()
    
    print("🌐 Menuju ke URL Gaelenlighten...")
    page.goto("https://lionairgroup.gaelenlighten.com/Home/Workspace#!/home")
    
    # Navigasi
    print("🖱️ Membuka menu navigasi...")
    page.locator("span").first.click()
    
    print("📊 Mengklik menu Business Intelligence...")
    page.get_by_role("link", name=" Business Intelligence").click()
    
    page.wait_for_timeout(5000)
    
    # Pencarian
    print("🔍 Mencari dashboard 'SRM_2026b'...")
    search_box = page.get_by_role("textbox", name="Enter your search term...")
    search_box.fill("SRM_2026b")
    search_box.press("Enter")
    
    page.wait_for_timeout(5000)

    print("🖱️ Memilih dashboard 'DASHBOARD IMR_Fariz_SRM_2026b'...")
    page.get_by_text("DASHBOARD IMR_Fariz_SRM_2026b").click()
    
    print("⏳ Menunggu dashboard loading (15 detik)...")
    page.wait_for_timeout(15000)
    
    print("📤 Mengklik tombol Export...")
    page.get_by_role("button", name="Export").click()
    page.wait_for_timeout(3000)
    
    print("📥 Memulai proses download (Menunggu hingga 60 detik)...")
    try:
        # Menambah timeout menjadi 60.000ms (60 detik) karena data berat
        with page.expect_download(timeout=600000) as download_info:
            # Kadang "Excel" diklik tidak langsung memunculkan popup, tapi langsung download
            # Kita fokus ke event download-nya saja
            page.get_by_text("Excel", exact=True).click()
            
        download = download_info.value
        
        # Penamaan file: SRM_Tanggal_NamaAsli.xlsx
        #timestamp = datetime.now().strftime("%Y%m%d_%H%M")
        #final_filename = f"SRM_{timestamp}_{download.suggested_filename}
        final_filename = "bi_fariz_bronze_layer.xls"
        save_path = os.path.join(download_dir, final_filename)
        
        download.save_as(save_path)
        print(f"✅ BERHASIL! File disimpan di: {save_path}")
        
    except Exception as e:
        print(f"❌ ERROR: Gagal download karena {e}")
        # Screenshot untuk debug jika error
        page.screenshot(path="error_download.png")
        print("📸 Screenshot error disimpan sebagai 'error_download.png'")

    print("🧹 Menutup browser...")
    context.close()
    browser.close()
    print("🏁 Selesai.")

with sync_playwright() as playwright:
    run(playwright)