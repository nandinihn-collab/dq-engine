from backend.db.snowflake_connector import run_query

def null_check(table_name: str):
    query = f"""
    SELECT 
        COUNT(*) AS total_rows,
        COUNT(*) - COUNT(BOOKING_ID) AS null_booking_id,
        COUNT(*) - COUNT(CUSTOMER_ID) AS null_customer_id,
        COUNT(*) - COUNT(BOOKING_STATUS) AS null_booking_status
    FROM {table_name}
    """

    return run_query(query)

def duplicate_details(table_name: str):
    from backend.db.snowflake_connector import run_query

    query = f"""
    SELECT BOOKING_ID, COUNT(*) as count
    FROM {table_name}
    GROUP BY BOOKING_ID
    HAVING COUNT(*) > 1
    """

    return run_query(query)
def duplicate_summary(table_name: str):
    from backend.db.snowflake_connector import run_query

    query = f"""
    SELECT COUNT(*) AS total_rows,
           COUNT(DISTINCT BOOKING_ID) AS unique_rows
    FROM {table_name}
    """

    result = run_query(query)

    if "error" in result:
        return result

    total = result[0]["total_rows"]
    unique = result[0]["unique_rows"]
    return {
        "total_rows": total,
        "unique_rows": unique,
        "duplicate_rows": total - unique
    }

def schema_validation(table_name: str):
    
    expected_columns = [
        "DATE",
        "TIME",
        "BOOKING_ID",
        "BOOKING_STATUS",
        "CUSTOMER_ID",
        "VEHICLE_TYPE",
        "PICKUP_LOCATION",
        "DROP_LOCATION"
    ]

    query = f"""
    SELECT COLUMN_NAME
    FROM INFORMATION_SCHEMA.COLUMNS
    WHERE TABLE_NAME = 'UBER_RIDE_DETAILS'
    """

    result = run_query(query)

    if "error" in result:
        return result

    actual_columns = [row["column_name"] for row in result]

    missing = [col for col in expected_columns if col not in actual_columns]

    return {
        "expected_columns": expected_columns,
        "actual_columns": actual_columns,
        "missing_columns": missing
    }

from datetime import datetime, timedelta
from backend.db.snowflake_connector import run_query

def timeliness_check(table_name: str, date_column: str):
    query = f"""
    SELECT 
        COUNT(*) AS TOTAL_ROWS,
        SUM(CASE 
            WHEN {date_column} < DATEADD(day, -30, CURRENT_DATE()) 
            THEN 1 ELSE 0 
        END) AS STALE_ROWS
    FROM {table_name}
    """
    return run_query(query)

def status_consistency_check(table_name: str):
    query = f"""
    SELECT booking_status, COUNT(*) AS COUNT
    FROM {table_name}
    WHERE LOWER(booking_status) NOT IN ('booked','completed','cancelled')
    GROUP BY booking_status
    """
    return run_query(query)

def rating_consistency_check(table_name: str):
    query = f"""
    SELECT COUNT(*) AS INVALID_RATINGS
    FROM {table_name}
    WHERE TRY_TO_NUMBER(driver_ratings) NOT BETWEEN 1 AND 5
       OR TRY_TO_NUMBER(customer_rating) NOT BETWEEN 1 AND 5
    """
    return run_query(query)

def numeric_consistency_check(table_name: str):
    query = f"""
    SELECT COUNT(*) AS INVALID_NUMERIC_ROWS
    FROM {table_name}
    WHERE TRY_TO_NUMBER(ride_distance) <= 0
       OR TRY_TO_NUMBER(booking_value) <= 0
    """
    return run_query(query)

def timeliness_check(table: str):
    query = f"""
    SELECT
        COUNT(*) AS TOTAL_ROWS,
        SUM(
            CASE
                WHEN TO_TIMESTAMP_NTZ(DATE || ' ' || TIME)
                     < DATEADD(day, -30, CURRENT_TIMESTAMP())
                THEN 1 ELSE 0
            END
        ) AS STALE_ROWS
    FROM {table}
    """
    return run_query(query)

def accuracy_check(table_name: str):
    query = f"""
    SELECT *
    FROM {table_name}
    WHERE 
        TRY_TO_NUMBER(RIDE_DISTANCE) < 0
        OR TRY_TO_NUMBER(BOOKING_VALUE) < 0
    """
    return run_query(query)

# def completeness_score(table: str):
#     query = f"""
#     SELECT
#         COUNT(*) AS TOTAL_ROWS,
#         SUM(
#             CASE WHEN BOOKING_ID IS NULL
#                OR CUSTOMER_ID IS NULL
#                OR VEHICLE_TYPE IS NULL
#                OR PICKUP_LOCATION IS NULL
#                OR DROP_LOCATION IS NULL
#             THEN 1 ELSE 0 END
#         ) AS INCOMPLETE_ROWS
#     FROM {table}
#     """
#     result = run_query(query)

#     if not result:
#         return {"error": "No data"}

#     total = result[0].get("total_rows") or result[0].get("total_rows", 0)
#     incomplete = result[0].get("incomplete_rows") or result[0].get("incomplete_rows", 0)

#     score = round(((total - incomplete) / total) * 100, 2) if total else 0

#     return {
#         "total_rows": total,
#         "incomplete_rows": incomplete,
#         "completeness_percent": score
#     }

def completeness_score(table: str):
    query = f"""
    SELECT
        COUNT(*) AS total_rows,
        SUM(
            CASE WHEN BOOKING_ID IS NULL
               OR CUSTOMER_ID IS NULL
               OR VEHICLE_TYPE IS NULL
               OR PICKUP_LOCATION IS NULL
               OR DROP_LOCATION IS NULL
            THEN 1 ELSE 0 END
        ) AS incomplete_rows
    FROM {table}
    """

    result = run_query(query)

    # ❗ If DB error occurred
    if isinstance(result, dict):
        return result

    # ❗ If no rows returned
    if not result:
        return {"error": "No data"}

    row = result[0]

    total = row.get("total_rows", 0)
    incomplete = row.get("incomplete_rows", 0)

    score = round(((total - incomplete) / total) * 100, 2) if total else 0

    return {
        "total_rows": total,
        "incomplete_rows": incomplete,
        "completeness_percent": score
    }

def consistency_check(table: str):
    query = f"""
    SELECT *
    FROM {table}
    WHERE 
        BOOKING_STATUS NOT IN ('COMPLETED','CANCELLED','ONGOING')
    """
    return run_query(query)