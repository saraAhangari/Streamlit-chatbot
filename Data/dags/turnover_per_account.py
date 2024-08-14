from collections import defaultdict
from datetime import datetime, timedelta

import psycopg2
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago

postgres_conn_config = {
    "user": "postgres",
    "password": "comeng2002",
    "host": "db",
    "port": "5432",
    "database": "finaldb",
}

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

turnover_per_account_type = defaultdict(float)


def fetch_data_from_postgres():
    DB_NAME = "stagedb"
    DB_USER = "postgres"
    DB_PASSWORD = "comeng2002"
    DB_HOST = "db"
    DB_PORT = "5432"

    connection = psycopg2.connect(
        dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT
    )
    cursor = connection.cursor()

    end_date = datetime.now()
    start_date = end_date - timedelta(days=1)

    try:
        cursor.execute(
            """
            SELECT
            amount, destination_account_type_name
            FROM
                staging.all_transactions
            WHERE
                transaction_date >= %s AND transaction_date < %s
        """,
            (start_date, end_date),
        )

        records = cursor.fetchall()

        for record in records:
            account_type = record["destination_account_type_name"]
            amount = record["amount"]
            turnover_per_account_type[account_type] += amount

    except Exception as e:
        print(f"Error fetching records: {e}")

    finally:
        cursor.close()
        connection.close()


def update_turnover_per_account_type():
    connection = psycopg2.connect(**postgres_conn_config)
    cursor = connection.cursor()

    try:
        for account_type, turnover in turnover_per_account_type.items():
            cursor.execute(
                """
                UPDATE staging.turnover_per_account_type
                SET
                    turnover = %s
                WHERE
                    ACCOUNT_TYPE_NAME = %s
            """,
                (turnover, account_type),
            )

        connection.commit()

    except Exception as e:
        print(f"Error updating turnover_per_account_type: {e}")
        connection.rollback()

    finally:
        cursor.close()
        connection.close()


with DAG(
    dag_id="daily_turnover_per_account",
    default_args=default_args,
    start_date=days_ago(2),
    schedule_interval="@daily",
    catchup=False,
) as dag:
    (
        PythonOperator(
            task_id="fetch_data_from_postgres",
            python_callable=fetch_data_from_postgres,
        )
        >> PythonOperator(
            task_id="update_turnover_per_account_type",
            python_callable=update_turnover_per_account_type,
            op_args=[],
        )
    )
