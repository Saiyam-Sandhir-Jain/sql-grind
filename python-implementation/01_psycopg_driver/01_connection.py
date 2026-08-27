import psycopg

from config import DATABASE_URL

with psycopg.connect(DATABASE_URL) as conn:
    print("Connected!")

    with conn.cursor() as cur:
        cur.execute("SELECT version();")
        result = cur.fetchone()
        print(result)