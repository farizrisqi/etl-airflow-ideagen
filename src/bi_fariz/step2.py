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

    target_columns = [
        "form_name", "DATE_TIME_OF_EVENT__UTC", "owner", "number",
        "EVENT_TITLE", "EVENT_DESCRIPTION", "Category", "status",
        "risk_rating_display_value", "submitted_date_time", "Risk_Event",
        "EVENT_LOCATION", "FROM", "TO", "JT_A_C_REGISTRATION",
        "IU_AC_REGISTRATION", "IW_A_C_REGISTRATION", "ID_A_C_REGISTRATION",
        "OD_A_C_REGISTRATION", "SL_A_C_REGISTRATION",
        "FLIGHT_NUMBER"
    ]

    try:
        # Kumpulkan semua file temp_sheet_*.csv yang dihasilkan ssconvert
        sheet_files = sorted([
            os.path.join(output_dir, f)
            for f in os.listdir(output_dir)
            if f.startswith("temp_sheet_") and f.endswith(".csv")
        ])

        if not sheet_files:
            print("❌ Error: Tidak ada sheet CSV yang ditemukan dari ssconvert.")
            return None

        print(f"📋 Ditemukan {len(sheet_files)} sheet: {[os.path.basename(f) for f in sheet_files]}")

        all_sheets = []
        for sheet_path in sheet_files:
            sheet_label = os.path.basename(sheet_path)
            print(f"🔄 Membaca {sheet_label}...")
            try:
                df_raw = pd.read_csv(sheet_path, skiprows=1)
                df_raw.columns = df_raw.columns.astype(str).str.strip()

                df_sheet = pd.DataFrame()
                for col in target_columns:
                    match = [i for i, c in enumerate(df_raw.columns) if c.lower() == col.lower()]
                    if match:
                        df_sheet[col] = df_raw.iloc[:, match[0]]
                    else:
                        df_sheet[col] = pd.NA

                if not df_sheet.dropna(how='all').empty:
                    all_sheets.append(df_sheet)
                    print(f"   ✅ {len(df_sheet)} baris diambil dari {sheet_label}")
                else:
                    print(f"   ⚠️ {sheet_label} kosong, dilewati.")
            except Exception as e:
                print(f"   ⚠️ Gagal membaca {sheet_label}: {e}")

        if not all_sheets:
            print("❌ Tidak ada data valid dari semua sheet.")
            return None

        df_total = pd.concat(all_sheets, ignore_index=True)
        print(f"🔗 Total baris setelah gabung semua sheet: {len(df_total)}")

        print("⚙️ Membersihkan format tanggal...")
        kolom_tanggal = ["DATE_TIME_OF_EVENT__UTC", "submitted_date_time"]
        for col in kolom_tanggal:
            if col in df_total.columns:
                df_total[col] = pd.to_datetime(df_total[col], errors='coerce').dt.strftime('%Y-%m-%d')

        base_name = os.path.splitext(os.path.basename(xls_path))[0]
        silver_name = base_name.replace("bronze", "silver")
        csv_output = os.path.join(output_dir, f"{silver_name}.csv")

        df_total.to_csv(csv_output, index=False)
        print(f"✨ Berhasil! Data Silver Layer tersimpan di: {csv_output}")

        for f in sheet_files:
            if os.path.exists(f):
                os.remove(f)

        return df_total

    except Exception as e:
        print(f"❌ Gagal memproses DataFrame: {e}")
        return None

# --- MAIN ---
if __name__ == "__main__":
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    path_file_baru = os.path.join(BASE_DIR, "Downloads_SRM", "bi_fariz_bronze_layer.xls")

    df_hasil = convert_to_silver_combined(path_file_baru)

    if df_hasil is not None:
        print("\n🔥 Selesai! Preview 5 Baris Pertama:")
        print(df_hasil[["DATE_TIME_OF_EVENT__UTC", "submitted_date_time"]].head())
