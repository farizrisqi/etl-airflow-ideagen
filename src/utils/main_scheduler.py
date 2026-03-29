import subprocess
import time
import sys 
from datetime import datetime

def run_script(script_name):
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] --- Memulai {script_name} ---")
    
    # PERBAIKAN: Menggunakan sys.executable agar otomatis 
    # menggunakan 'python3' sesuai lingkungan terminalmu
    result = subprocess.run([sys.executable, script_name])
    
    if result.returncode == 0:
        print(f"--- {script_name} Berhasil Selesai ---")
    else:
        print(f"--- {script_name} Berhenti dengan Error ---")

print("\nJalankan Project ETL untuk menarik Report Terbaru\n")
print("\nTarik Data OPS Report\n")
run_script("tarik_opsreport.py")
print("\nTarik Data Ideagen Report\n")
run_script("tarik_ideagen_pertama.py")
print("\nMenunggu 10 menit agar filenya muncul...\n")
time.sleep(600)
run_script("tarik_ideagen_kedua.py")
print("\nFile sudah terdownload, lanjut proses Transform data\n")
run_script("tarik_ideagen_ketiga.py")
print("\nFile sudah terdownload, lanjut proses Load data ke CMR \n")
run_script("tarik_ideagen_keempat.py")
