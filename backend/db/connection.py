import sqlite3

def get_connection():
    conn = sqlite3.connect("rides.db")
    return conn

def run_query(query: str):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(query)
        rows = cursor.fetchall()

        columns = [desc[0] for desc in cursor.description]

        results = []
        for row in rows:
            results.append(dict(zip(columns, row)))

        return results

    except Exception as e:
        return {"error": str(e)}

    finally:
        conn.close()