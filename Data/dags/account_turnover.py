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

stagedb_conn_config = {
    "user": "postgres",
    "password": "comeng2002",
    "host": "db",
    "port": "5432",
    "database": "stagedb",
}

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

daily_total_turnover_per_account = defaultdict(float)


def fetch_data_from_postgres():
    connection = psycopg2.connect(**stagedb_conn_config)

    cursor = connection.cursor()

    end_date = datetime.now()
    start_date = end_date - timedelta(days=1)

    try:
        cursor.execute(
            """
            SELECT
            transaction_date, account_number, customer_name
            FROM
                staging.all_transactions
            WHERE
                transaction_date >= %s AND transaction_date < %s
        """,
            (start_date, end_date),
        )

        records = cursor.fetchall()

        for record in records:
            transaction_date = record["transaction_date"].date()
            print(transaction_date)

            account_number = record["account_number"]
            customer_name = record["customer_name"]
            amount = record["amount"]

            daily_total_turnover_per_account[
                (account_number, customer_name, transaction_date)
            ] += amount

    except Exception as e:
        print(f"Error fetching records: {e}")

    finally:
        cursor.close()
        connection.close()


def update_account_turnover():
    connection = psycopg2.connect(**postgres_conn_config)
    cursor = connection.cursor()

    try:
        for (
            account_number,
            transaction_date,
            customer_name,
        ), daily_total_turnover in daily_total_turnover_per_account.items():
            cursor.execute(
                """
                UPDATE staging.account_turnover
                SET
                    total_amount = %s
                WHERE
                    account_id = %s
                    customer_name = %s
                    AND date = %s
            """,
                (daily_total_turnover, account_number, customer_name, transaction_date),
            )

        connection.commit()

    except Exception as e:
        print(f"Error updating account_turnover: {e}")
        connection.rollback()

    finally:
        cursor.close()
        connection.close()


with DAG(
    dag_id="daily_account_turnover",
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
            task_id="update_account_turnover",
            python_callable=update_account_turnover,
            op_args=[],
        )
    )
