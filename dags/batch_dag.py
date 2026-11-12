"""BATCH : charge les 3 fichiers CSV dans le schéma raw."""
from datetime import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator

from db import get_conn


def load_csv(table):
    conn = get_conn()
    with conn, conn.cursor() as cur, open(f"/opt/airflow/data/{table}.csv", encoding="utf-8") as f:
        columns = f.readline().strip()   # 1re ligne = noms des colonnes
        f.seek(0)                        # on revient au début du fichier
        cur.execute(f"TRUNCATE raw.{table}")   # on vide = relançable sans risque
        cur.copy_expert(f"COPY raw.{table} ({columns}) FROM STDIN WITH CSV HEADER", f)
    conn.close()
    print(f"raw.{table} chargée")


with DAG(
    dag_id="2_batch",
    schedule="@daily",
    start_date=datetime(2026, 1, 1),
    catchup=False,
    tags=["indrive"],
) as dag:
    for table in ["drivers", "vehicles", "zones"]:
        PythonOperator(task_id=f"load_{table}", python_callable=load_csv, op_args=[table])