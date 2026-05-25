import pandas as pd
import os
import subprocess

def convert_to_silver_combined(xls_path):
    print(f"🚀 Memproses file: {xls_path}")

    if not os.path.exists(xls_path):
        print(f"❌ Error: File {xls_path} tidak ditemukan!")
        return None

    output_dir = os.path.dirname(xls_path) or "."

    template_csv = os.path.join(output_dir, "temp_sheet_%n.csv")

    try:
        print("🔄 Mengekstrak SEMUA sheet sekaligus via ssconvert...")
        subprocess.run(
            ['ssconvert', '-S', xls_path, template_csv],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        print("✅ Ekstraksi semua sheet berhasil!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Gagal ekstraksi: {e.stderr.decode()}")
        return None
    except FileNotFoundError:
        print("❌ Error: Perintah 'ssconvert' tidak ditemukan. Jalankan 'sudo apt install gnumeric' di terminal WSL.")
        return None

    temp_s1 = os.path.join(output_dir, "temp_sheet_0.csv")

    target_columns = [
        "owner",
        "DATE_TIME_OF_EVENT__UTC",
        "opened_date_time",
        "number",
        "SHOR_EVENT_TITLE",
        "SHOR_EVENT_DESCRIPTION",
        "Category",
        "status",
        "risk_rating_display_value",
        "submitted_date_time",
        "EMAIL",
        "Workflow_Stage_Title",
        "Workflow_Stage_response"
    ]

    try:
        if not os.path.exists(temp_s1):
            print("❌ Error: Sheet pertama (index 0) tidak ditemukan.")
            return None

        print("🔄 Membaca data Sheet 1...")
        df1_raw = pd.read_csv(temp_s1, skiprows=1)
        df1_raw.columns = df1_raw.columns.astype(str).str.strip()

        df1_final = pd.DataFrame()

        for col in target_columns:
            match = [i for i, c in enumerate(df1_raw.columns) if c.lower() == col.lower()]
            if match:
                df1_final[col] = df1_raw.iloc[:, match[0]]
            else:
                df1_final[col] = pd.NA

        print("⚙️ Membersihkan format tanggal...")
        kolom_tanggal = ["DATE_TIME_OF_EVENT__UTC", "opened_date_time", "submitted_date_time"]
        for col in kolom_tanggal:
            if col in df1_final.columns:
                df1_final[col] = pd.to_datetime(df1_final[col], errors='coerce').dt.strftime('%Y-%m-%d')

        df_total = df1_final

        base_name = os.path.splitext(os.path.basename(xls_path))[0]
        silver_name = base_name.replace("bronze", "silver")
        json_output = os.path.join(output_dir, f"{silver_name}.json")

        df_total.to_json(json_output, orient='records', indent=4, force_ascii=False)
        print(f"✨ Berhasil! Data Silver Layer tersimpan di: {json_output}")

        if os.path.exists(temp_s1):
            os.remove(temp_s1)

        return df_total

    except Exception as e:
        print(f"❌ Gagal memproses DataFrame: {e}")
        return None

# --- MAIN ---
if __name__ == "__main__":
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    path_file_baru = os.path.join(BASE_DIR, "Downloads_SRM", "bi_srm_bronze_layer.xls")

    df_hasil = convert_to_silver_combined(path_file_baru)

    if df_hasil is not None:
        print("\n🔥 Selesai! Preview 5 Baris Pertama:")
        print(df_hasil[["DATE_TIME_OF_EVENT__UTC", "opened_date_time", "submitted_date_time"]].head())
