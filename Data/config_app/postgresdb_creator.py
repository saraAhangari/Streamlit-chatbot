import psycopg2

# Database connection parameters
DB_NAME = "postgres"
DB_USER = "postgres"
DB_PASSWORD = "comeng2002"
DB_HOST = "db"
DB_PORT = "5432"


def run_source_sql(filename):
    """
    Connect to the database
    And run the scripts in the file
    """
    conn = psycopg2.connect(
        dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT
    )
    conn.autocommit = True

    with open(filename, "r") as file:
        sql_script = file.read()

    cursor = conn.cursor()
    cursor.execute(sql_script)
    cursor.close()

    conn.close()
    print("postgres - Your queries executed successfully.\n")


run_source_sql("postgresdb.sql")
