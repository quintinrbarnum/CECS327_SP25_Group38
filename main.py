import pandas as pd
import psycopg2 as pg
from psycopg2 import pool
import json

def main():
     
     
     connection_string = "postgresql://neondb_owner:npg_opgQ23NvUrLC@ep-icy-band-a5auz6ag-pooler.us-east-2.aws.neon.tech/neondb?sslmode=require"
     connect = pool.SimpleConnectionPool(1,10, connection_string)

     if connect:
          conn = connect.getconn()
          cur = conn.cursor()

          cur.execute('SELECT * FROM "ProjectEight_virtual" LIMIT 5;')
          rows = cur.fetchall()
          colnames = [desc[0] for desc in cur.description]
          df = pd.DataFrame(rows, columns=colnames)
          #convert columns with timezone to ExcelWriteable
          for col in df.select_dtypes(include=['datetimetz']):
               df[col] = df[col].dt.tz_localize(None)
          payload = df["payload"].apply(pd.Series)
          df = pd.concat([df.drop(columns=["payload"]), payload], axis=1)
          df.to_excel('ProjectEight_virtual.xlsx', index=False)
          
          conn.close()


if __name__ == "__main__":
    main()
