import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# Database connection parameters
DB_NAME = "postgres"
DB_USER = "postgres"
DB_PASSWORD = "comeng2002"
DB_HOST = "db"
DB_PORT = "5432"


def run_source_sql():
    """
    Connect to the database
    And run the scripts in the file
    """
    conn = psycopg2.connect(
        dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT
    )
    conn.autocommit = True

    cursor = conn.cursor()
    stage_query = "create database stagedb;"
    cursor.execute(stage_query)
    conn.commit()

    finaldb_query = "create database finaldb;"
    cursor.execute(finaldb_query)
    conn.commit()
    cursor.close()

    conn.close()
    print("Create Databases - Your queries executed successfully.\n")


run_source_sql()
