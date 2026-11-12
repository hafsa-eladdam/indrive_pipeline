"""STAGING : attend les sources, nettoie en parallèle, puis déclenche les marts."""
from datetime import datetime

from airflow import DAG
from airflow.models import DagRun
from airflow.operators.python import PythonOperator
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
from airflow.sensors.python import PythonSensor
from airflow.utils.state import DagRunState

from db import run_sql_file


def sources_ready():
    """Vrai si 1_streaming ET 2_batch ont réussi au moins une fois."""
    for dag_id in ("1_streaming", "2_batch"):
        if not DagRun.find(dag_id=dag_id, state=DagRunState.SUCCESS):
            return False
    return True


with DAG(
    dag_id="3_staging",
    schedule="*/2 * * * *",          # toutes les 2 minutes
    start_date=datetime(2026, 1, 1),
    catchup=False,
    max_active_runs=1,
    tags=["indrive"],
) as dag:

    wait_for_sources = PythonSensor(
        task_id="wait_for_sources",
        python_callable=sources_ready,
        poke_interval=30,
        mode="reschedule",
    )

    stg_tasks = [
        PythonOperator(
            task_id=f"stg_{name}",
            python_callable=run_sql_file,
            op_args=[f"staging/{name}.sql"],
        )
        for name in ("drivers", "vehicles", "zones", "rides")
    ]

    trigger_marts = TriggerDagRunOperator(
        task_id="trigger_marts",
        trigger_dag_id="4_marts",
    )

    wait_for_sources >> stg_tasks >> trigger_marts