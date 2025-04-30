import pandas as pd
import psycopg2 as pg
from psycopg2 import pool

def main():
     connection_string = "postgresql://neondb_owner:npg_opgQ23NvUrLC@ep-icy-band-a5auz6ag-pooler.us-east-2.aws.neon.tech/neondb?sslmode=require"
     connect = pool.SimpleConnectionPool(1,10, connection_string)

     if connect:
          conn = connect.getconn()
          cur = conn.cursor()

          cur.execute('SELECT * FROM "ProjectEight_virtual";')
          rows = cur.fetchall()
          #colnames = [desc[0] for desc in cur.description]
          for row in rows:
               print(row)


if __name__ == "__main__":
    main()
