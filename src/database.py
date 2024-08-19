import logging
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from sqlalchemy.exc import SQLAlchemyError

def get_postgres_connection(config: dict) -> Engine:
    """
    Establish a connection to the PostgreSQL database.

    Args:
        config (dict): Configuration dictionary containing database connection details.

    Returns:
        Engine: SQLAlchemy Engine object for the PostgreSQL connection, or None if the connection fails.
    """
    try:
        engine = create_engine(
            f"postgresql://{config['user']}:{config['password']}@{config['host']}:{config['port']}/{config['dbname']}"
        )
        return engine
    except SQLAlchemyError as e:
        logging.error(f"Database connection failed: {e}")
        return None

def query_user_data(engine: Engine, account_number: str) -> dict:
    """
    Query the user's data from the database using the account number.

    Args:
        engine (Engine): SQLAlchemy Engine object for database interaction.
        account_number (str): The user's account number.

    Returns:
        dict: Dictionary containing 'turnover' and 'customer_name' if found, otherwise None.
    """
    query = text("SELECT turnover, customer_name FROM facts.account_turnover WHERE account_no = :account_number")
    try:
        with engine.connect() as connection:
            result = connection.execute(query, {'account_number': int(account_number)})
            user_data = result.fetchone()
            return {'turnover': user_data[0], 'customer_name': user_data[1]} if user_data else None
    except SQLAlchemyError as e:
        logging.error(f"Query failed: {e}")
        return None
