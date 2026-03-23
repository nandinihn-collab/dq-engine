from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv
load_dotenv()

def get_engine():
    user = os.getenv("SNOWFLAKE_USER")
    password = os.getenv("SNOWFLAKE_PASSWORD")
    account = os.getenv("SNOWFLAKE_ACCOUNT")
    warehouse = os.getenv("SNOWFLAKE_WAREHOUSE")
    database = os.getenv("SNOWFLAKE_DATABASE")
    schema = os.getenv("SNOWFLAKE_SCHEMA")

    connection_string = f"snowflake://{user}:{password}@{account}/{database}/{schema}?warehouse={warehouse}"

    engine = create_engine(connection_string)
    return engine


def run_query(query: str):
    engine = get_engine()

    try:
        with engine.connect() as conn:
            result = conn.execute(text(query))   

            columns = result.keys()
            rows = result.fetchall()

            return [dict(zip(columns, row)) for row in rows]

    except Exception as e:
        return {"error": str(e)}