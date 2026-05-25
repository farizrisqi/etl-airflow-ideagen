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
    dag_id='bi_fariz_manual',
    default_args=default_args,
    description='Manual trigger ETL khusus BI Fariz (step1 → step2 → step3)',
    schedule=None,
    catchup=False,
    is_paused_upon_creation=True,
    tags=['etl', 'scraping', 'playwright', 'bi_fariz'],
) as dag:

    BASE_CMD = "cd /opt/airflow/src/bi_fariz && python"

    bi_step_1 = BashOperator(
        task_id='bi_step_1',
        bash_command=f'{BASE_CMD} step1.py',
        retries=0,
    )

    bi_step_2 = BashOperator(
        task_id='bi_step_2',
        bash_command=f'{BASE_CMD} step2.py',
        retries=0,
    )

    bi_step_3 = BashOperator(
        task_id='bi_step_3',
        bash_command=f'{BASE_CMD} step3.py',
        retries=0,
    )

    bi_step_1 >> bi_step_2 >> bi_step_3
