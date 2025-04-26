import time
import psycopg2

# Wait until DB is up
while True:
    try:
        conn = psycopg2.connect(
            host="user_db",
            port=5432,
            user="postgres",
            password="postgres",
            dbname="userdb"
        )
        print("PostgreSQL is ready!")
        conn.close()
        break
    except psycopg2.OperationalError:
        print("Waiting for PostgreSQL to start...")
        time.sleep(2)
