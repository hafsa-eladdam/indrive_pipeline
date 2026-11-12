"""Petits helpers partagés par les 4 DAGs."""
import os

import psycopg2  # type: ignore


def get_conn():
    """Ouvre une connexion à Postgres."""
    return psycopg2.connect(
        host=os.environ["PG_HOST"],
        dbname=os.environ["PG_DB"],
        user=os.environ["PG_USER"],
        password=os.environ["PG_PASSWORD"],
    )


def run_sql_file(path):
    """Exécute un fichier .sql du dossier sql/."""
    with open(f"/opt/airflow/sql/{path}", encoding="utf-8") as f:
        sql = f.read()
    conn = get_conn()
    with conn, conn.cursor() as cur:   # "with conn" = commit à la fin
        cur.execute(sql)
    conn.close()