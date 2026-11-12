"""STREAMING : toutes les minutes, appelle une API et stocke les courses dans raw.rides."""
import os
import random
from datetime import datetime

import requests
from airflow import DAG
from airflow.operators.python import PythonOperator

from db import get_conn


def pull_rides():
    # UN appel : l'API renvoie 10 faux paniers (ils ne servent que de "déclencheur")
    url = f"https://dummyjson.com/carts?limit=10&skip={random.randint(0, 190)}"
    verify = os.environ.get("VERIFY_SSL", "true") == "true"   # voir plus bas si ton réseau bloque HTTPS
    carts = requests.get(url, timeout=10, verify=verify).json()["carts"]

    now = datetime.utcnow()
    conn = get_conn()
    with conn, conn.cursor() as cur:
        for cart in carts:
            ride_id = f"ride_{now:%Y%m%d%H%M%S}_{cart['id']}"   # 1 panier = 1 course

            # ~5 % des courses pointent vers un chauffeur qui n'existe pas
            if random.random() < 0.05:
                driver_id = 999
            else:
                driver_id = random.randint(1, 8)                # nos 8 chauffeurs

            pickup_zone_id = random.randint(1, 8)               # nos 8 zones
            dropoff_zone_id = random.randint(1, 8)
            distance_km = round(random.uniform(1, 25), 1)

            # ~3 % des courses ont un tarif à 0 (pour tester le filtre du staging)
            if random.random() < 0.03:
                fare_amount = 0
            else:
                fare_amount = round(10 + distance_km * random.uniform(3, 6), 2)

            cur.execute(
                "INSERT INTO raw.rides VALUES (%s, %s, %s, %s, %s, %s, %s)",
                [ride_id, driver_id, pickup_zone_id, dropoff_zone_id, now, distance_km, fare_amount],
            )
    conn.close()
    print(f"{len(carts)} courses enregistrées dans raw.rides")


with DAG(
    dag_id="1_streaming",
    schedule="* * * * *",          # toutes les minutes
    start_date=datetime(2026, 1, 1),
    catchup=False,
    max_active_runs=1,
    tags=["indrive"],
) as dag:
    PythonOperator(task_id="pull_rides", python_callable=pull_rides)