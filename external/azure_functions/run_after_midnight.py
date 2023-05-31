import datetime
import logging
import requests
import time
import pandas as pd
import azure.functions as func
import psycopg2
from psycopg2.extras import execute_values
import os
from dotenv import load_dotenv


def main(mytimer: func.TimerRequest) -> None:
    midnight = int(divmod(time.time(), 3600*24)[0] * 3600*24)

    response = requests.get(f'https://opensky-functions.azurewebsites.net/api/delete_old_flights?time={midnight}')

    for i in range(12):
        response = requests.get(f"https://opensky-network.org/api/flights/all?begin={midnight-((i+1)*7200)}&end={midnight-(i*7200)}")
        response_body = response.json()

        df = pd.DataFrame.from_records(response_body)
        aircraft = pd.DataFrame({'icao24':df.icao24,'operator_id':[0]*len(df.icao24),'manufacturer':['Null']*len(df.icao24),'model':['Null']*len(df.icao24)})
        conn = psycopg2.connect(database=os.environ['PG_DATABASE'], user=os.environ['PG_USERNAME'], password=os.environ['PG_PASSWORD'], 
                                host=os.environ['PG_HOST'], port=os.environ['PG_PORT'])

        with conn.cursor() as cursor:
            columns = aircraft.columns.tolist()
            values = [tuple(row) for row in aircraft.values]
            insert_sql = f"INSERT INTO Aircraft ({', '.join(columns)}) VALUES %s ON CONFLICT (icao24) DO NOTHING"
            execute_values(cursor, insert_sql, values)
            conn.commit()

            columns = df.columns.tolist()
            values = [tuple(row) for row in df.values]
            insert_sql = f"INSERT INTO Flight ({', '.join(columns)}) VALUES %s ON CONFLICT (icao24, firstSeen) DO UPDATE SET ({', '.join(columns[2:])}) = ({', '.join(['excluded.'+ c for c in columns[2:]])})"
            execute_values(cursor, insert_sql, values)
            conn.commit()
        conn.close()

        time.sleep(5)

    response = requests.put('http://35.176.80.148/flights')