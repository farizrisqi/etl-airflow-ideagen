from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

# Konfigurasi dasar DAG
default_args = {
    'owner': 'fariz',
    'depends_on_past': False,
    'start_date': datetime(2026, 2, 1), # Tanggal mulai ditarik mundur sedikit agar siap jalan
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    dag_id='master_dag_auto_etl',
    default_args=default_args,
    description='Automasi ETL Tarik Data OpsReport dan Ideagen',
    schedule_interval='0 4 * * 1-5', # Berjalan setiap jam 04:00 pagi, Senin - Jumat
    catchup=False,
    tags=['etl', 'scraping', 'playwright']
) as dag:

    # PENTING: Kita gunakan perintah 'cd' ke folder repo terlebih dahulu 
    # agar kalau ada file hasil download/output, tersimpan di folder yang benar.
    # {{ dags_folder }} adalah variabel bawaan Airflow untuk menunjuk ke folder 'dags'
    
    BASE_CMD = "cd {{ dags_folder }}/auto-etl-airflow && python"

    tarik_opsreport = BashOperator(
        task_id='tarik_opsreport',
        bash_command=f'{BASE_CMD} tarik_opsreport.py'
    )

    tarik_ideagen_pertama = BashOperator(
        task_id='tarik_ideagen_pertama',
        bash_command=f'{BASE_CMD} tarik_ideagen_pertama.py'
    )

    # Pengganti time.sleep(600)
    jeda_10_menit = BashOperator(
        task_id='menunggu_file_muncul',
        bash_command='sleep 600'
    )

    tarik_ideagen_kedua = BashOperator(
        task_id='tarik_ideagen_kedua',
        bash_command=f'{BASE_CMD} tarik_ideagen_kedua.py'
    )

    tarik_ideagen_ketiga = BashOperator(
        task_id='tarik_ideagen_ketiga',
        bash_command=f'{BASE_CMD} tarik_ideagen_ketiga.py'
    )

    tarik_ideagen_keempat = BashOperator(
        task_id='tarik_ideagen_keempat',
        bash_command=f'{BASE_CMD} tarik_ideagen_keempat.py'
    )

    # Mengatur urutan jalan (Dependencies) sama persis seperti main_scheduler.py
    (
        tarik_opsreport 
        >> tarik_ideagen_pertama 
        >> jeda_10_menit 
        >> tarik_ideagen_kedua 
        >> tarik_ideagen_ketiga 
        >> tarik_ideagen_keempat
    )
