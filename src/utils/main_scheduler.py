import subprocess
import time
import sys
import os
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IDEAGEN_DIR = os.path.join(BASE_DIR, "..", "ideagen")
BI_FARIZ_DIR = os.path.join(BASE_DIR, "..", "bi_fariz")
BI_SRM_DIR   = os.path.join(BASE_DIR, "..", "bi_srm")

def run_script(script_name, cwd):
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] --- Memulai {script_name} ---")
    result = subprocess.run([sys.executable, script_name], cwd=cwd)
    if result.returncode == 0:
        print(f"--- {script_name} Berhasil ---")
    else:
        print(f"--- {script_name} Error (return code {result.returncode}) ---")

print("\n=== ETL Pipeline Start ===\n")

run_script("opsreport_step_1.py", IDEAGEN_DIR)
run_script("ideagen_step_1.py",   IDEAGEN_DIR)

print("\nMenunggu 10 menit agar file muncul...\n")
time.sleep(600)

run_script("ideagen_step_2.py", IDEAGEN_DIR)
run_script("ideagen_step_3.py", IDEAGEN_DIR)
run_script("ideagen_step_4.py", IDEAGEN_DIR)

run_script("step1.py", BI_FARIZ_DIR)
run_script("step2.py", BI_FARIZ_DIR)
run_script("step3.py", BI_FARIZ_DIR)

run_script("step1.py", BI_SRM_DIR)
run_script("step2.py", BI_SRM_DIR)
run_script("step3.py", BI_SRM_DIR)

print("\n=== ETL Pipeline Selesai ===\n")
