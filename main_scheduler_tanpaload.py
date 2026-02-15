import subprocess
import time
import sys # Tambahkan ini
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

print("\nJalankan Project ETL untuk menarik Report Terbaru langsung dari proses 2\n")
run_script("tarik_ideagen_kedua.py")
print("\nFile sudah terdownload, lanjut proses Transform data\n")
time.sleep(10)
run_script("tarik_ideagen_ketiga.py")
print("\nFile sudah terdownload, lanjut proses Load data ke CMR \n")
time.sleep(10)
run_script("tarik_ideagen_keempat.py")
