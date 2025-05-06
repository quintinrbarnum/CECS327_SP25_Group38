import pandas as pd
import psycopg2 as pg
from psycopg2 import pool
import json
import socket, ipaddress

def main():
     baseQuery = """ SELECT * FROM "ProjectEight_virtual" LIMIT 5; """
     fridgeQuery = """ SELECT AVG(("payload" ->> 'Moisture Meter - Moisture Meter')::FLOAT ) FROM "ProjectEight_virtual" WHERE "createdAt" >= NOW() - INTERVAL '3 hours' AND  "payload"->>'board_name' = 'Fridge 1 Board'; """
     waterQuery = """ SELECT AVG(("payload" ->> 'YF-S201 - water sensor')::FLOAT ) FROM "ProjectEight_virtual" WHERE "payload"->>'board_name' = 'dishwasher board'; """
     sumQuery = """ SELECT SUM(("payload" ->> 'sensor 1 1098a70b-0f85-4c9b-81f3-e2c7069eacd7')::FLOAT) as "Dishwasher",
     SUM(("payload" ->> 'sensor 1 8a864328-e3b8-4ffa-ad2c-ce630139d944')::FLOAT) as "Fridge 2",
     SUM(("payload" ->> 'ACS712 - Ammeter')::FLOAT) as "Fridge 1" FROM "ProjectEight_virtual" ;
     """
     connection_string = "postgresql://neondb_owner:npg_opgQ23NvUrLC@ep-icy-band-a5auz6ag-pooler.us-east-2.aws.neon.tech/neondb?sslmode=require"
     #Ensure that host can connect
     host = "0.0.0.0"
     port = int(input("Enter the port number to run the server on: "))
     server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
     server_socket.bind((host, port))
     server_socket.listen(5)
     print("Waiting on port", port)
     while True:
          response = True
          client_socket, client_address = server_socket.accept()
          print("Connection established with", client_address)
          while response: 
               data = client_socket.recv(1024).decode()
               if not data:
                    print("Client disconnected")
                    break
               if(data == "1" or data.lower() == "average moisture"):
                    response = avg(connection_string, fridgeQuery)
                    final_str = "Average Moisture in the past three hours: " + str(response) + "%"
               elif(data == "2" or data.lower() == "average water consumption"):
                    response = avg(connection_string, waterQuery)
                    final_str = "average water consumption of dishwasher: " + str(response) + " Gallons"
               elif(data == "3" or data.lower() == "most electricity consumed"):
                    response = find_sum(connection_string, sumQuery)
                    maximum = max(response)
                    final_str = "Most Electricity Consumed: " + str(maximum) + " Watts"
               else:
                    final_str =  "Invalid Query please select one of the options available!"
               client_socket.send(final_str.encode())
          
     
def find_sum(connect_string, query):
     connect = pool.SimpleConnectionPool(1,10, connect_string)
     if connect:
          conn = connect.getconn()
          cur = conn.cursor()
          cur.execute(query)
          rows = cur.fetchall()
          return rows[0]
     else: 
          return None
          
def avg(connect_string, query):
    connect = pool.SimpleConnectionPool(1,10, connect_string)
    if connect:
        conn = connect.getconn()
        cur = conn.cursor()
        cur.execute(query)
        avg = cur.fetchone()[0]
        conn.close()
        return avg
    else:
        return None


if __name__ == "__main__":
    main()
