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

print("\nJalankan Project ETL untuk menarik Data Business Intelligence\n")
print("\nJalankan Step 1\n")
run_script("step1.py")
print("\nJalankan Step 2\n")
run_script("step2.py")
print("\nJalankan Step 3\n")
run_script("step3.py")