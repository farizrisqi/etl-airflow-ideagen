from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'fariz',
    'depends_on_past': False,
    'start_date': datetime(2026, 4, 1),
    'retries': 0,
    'retry_delay': timedelta(minutes=1),
}

with DAG(
    dag_id='master_dag_etl-srm',
    default_args=default_args,
    description='Automasi ETL Tarik Data OpsReport dan Ideagen',
    schedule='30 0 * * 1-5',  # 07:30 WIB Senin-Jumat
    catchup=False,
    is_paused_upon_creation=False,
    tags=['etl', 'scraping', 'playwright']
) as dag:

    BASE_CMD_IDEAGEN = "cd /opt/airflow/src/ideagen && python"
    BASE_CMD_BI_FARIZ = "cd /opt/airflow/src/bi_fariz && python"
    BASE_CMD_BI_SRM   = "cd /opt/airflow/src/bi_srm && python"

    # ── OpsReport ────────────────────────────────────────────────
    opsreport_step_1 = BashOperator(
        task_id='opsreport_step_1',
        bash_command=f'{BASE_CMD_IDEAGEN} opsreport_step_1.py',
        retries=0,
    )

    # ── Ideagen ──────────────────────────────────────────────────
    ideagen_step_1 = BashOperator(
        task_id='ideagen_step_1',
        bash_command=f'{BASE_CMD_IDEAGEN} ideagen_step_1.py',
        retries=0,
    )

    jeda_10_menit = BashOperator(
        task_id='jeda_10_menit',
        bash_command='sleep 600',
        retries=0,
    )

    ideagen_step_2 = BashOperator(
        task_id='ideagen_step_2',
        bash_command=f'{BASE_CMD_IDEAGEN} ideagen_step_2.py',
        retries=0,
    )

    ideagen_step_3 = BashOperator(
        task_id='ideagen_step_3',
        bash_command=f'{BASE_CMD_IDEAGEN} ideagen_step_3.py',
        retries=0,
    )

    ideagen_step_4 = BashOperator(
        task_id='ideagen_step_4',
        bash_command=f'{BASE_CMD_IDEAGEN} ideagen_step_4.py',
        retries=0,
    )

    # ── BI Fariz ─────────────────────────────────────────────────
    bi_step_1 = BashOperator(
        task_id='bi_step_1',
        bash_command=f'{BASE_CMD_BI_FARIZ} step1.py',
        retries=0,
    )

    bi_step_2 = BashOperator(
        task_id='bi_step_2',
        bash_command=f'{BASE_CMD_BI_FARIZ} step2.py',
        retries=0,
    )

    bi_step_3 = BashOperator(
        task_id='bi_step_3',
        bash_command=f'{BASE_CMD_BI_FARIZ} step3.py',
        retries=0,
    )

    # ── BI SRM ───────────────────────────────────────────────────
    bi_srm_step_1 = BashOperator(
        task_id='bi_srm_step_1',
        bash_command=f'{BASE_CMD_BI_SRM} step1.py',
        retries=0,
    )

    bi_srm_step_2 = BashOperator(
        task_id='bi_srm_step_2',
        bash_command=f'{BASE_CMD_BI_SRM} step2.py',
        retries=0,
    )

    bi_srm_step_3 = BashOperator(
        task_id='bi_srm_step_3',
        bash_command=f'{BASE_CMD_BI_SRM} step3.py',
        retries=0,
    )

    # ── Dependencies ─────────────────────────────────────────────
    opsreport_step_1 >> ideagen_step_1 >> [jeda_10_menit, bi_step_1, bi_srm_step_1]
    bi_step_1 >> bi_step_2 >> bi_step_3
    bi_srm_step_1 >> bi_srm_step_2 >> bi_srm_step_3
    [jeda_10_menit, bi_step_3, bi_srm_step_3] >> ideagen_step_2
    ideagen_step_2 >> ideagen_step_3 >> ideagen_step_4