import io
import pandas as pd
import requests
from psycopg2.extras import execute_values
from connection_string import create_postgres_conn
from datetime import datetime


def get_data():
    r = requests.get(f'https://opensky-network.org/datasets/metadata/aircraft-database-complete-{datetime.now().year}-{"{:02d}".format(datetime.now().month)}.csv')
    aircraft_initial = pd.read_csv(io.BytesIO(r.content),encoding='ISO-8859-1',names=['icao24','registration','icao_part_1','manufacturer','model',
                                                                                         'icao_part2','delete','delete2','icao_part3','owner','airline_callsign',
                                                                                         'airline_icao','iata','operator','receiver'],
                                                                                         skiprows=1)
    codes = pd.read_csv('static/data/prefix_codes.csv',header=0)
    codes = codes.reset_index(names='country_id')

    aircraft_initial = aircraft_initial.drop(['delete','delete2','owner','iata','icao_part_1','icao_part2','icao_part3','receiver'],axis=1)

    r = requests.get('https://davidmegginson.github.io/ourairports-data/airports.csv')
    airports = pd.read_csv(io.BytesIO(r.content))
    airports = airports[['ident','type','name','latitude_deg','longitude_deg','iso_country','municipality']].rename(columns={'ident':'icao','name':'airport','latitude_deg':'latitude','longitude_deg':'longitude'})

    return aircraft_initial, codes, airports


def get_tables():
    aircraft_initial, codes, airports = get_data()

    countries = []
    for aircraft in aircraft_initial['registration']:
        found = False
        for prefix, country_id in zip(codes['Regn Prefix'],codes['country_id']):
            if str(aircraft).startswith(prefix):
                countries.append(country_id)
                found = True
                break
        if not found:
            countries.append(None)
    aircraft_initial['country_id'] = countries
    aircraft = aircraft_initial.reset_index(names='aircraft_id')
    aircraft = aircraft.loc[(aircraft['icao24'].str.len() == 6)]

    operator = aircraft.drop_duplicates(subset=['airline_callsign','airline_icao','operator','country_id']).drop(['aircraft_id','icao24','registration','manufacturer','model'],axis=1).reset_index(drop=True).reset_index(names='operator_id')

    new_aircraft = pd.merge(aircraft,operator,on=['airline_callsign','airline_icao','operator','country_id']).drop(['airline_callsign','airline_icao','operator','country_id','aircraft_id'],axis=1)
    new_aircraft = new_aircraft.drop(['registration'],axis=1)

    operator = operator.rename(columns={'airline_callsign':'callsign','airline_icao':'icao'})
    operator.country_id = operator.country_id.astype('Int64')
    operator.country_id = operator.country_id.fillna(-1).astype(str).replace('-1', 'NaN')
    operator.country_id = operator.country_id.replace('NaN', None)

    countries = codes[['country_id','Country Name','ISO Country Code']].rename(columns={'Country Name': 'country','ISO Country Code':'ISO'})

    airports = pd.merge(airports,countries[['ISO','country_id']],left_on='iso_country',right_on='ISO').drop(['iso_country','ISO'],axis=1).drop_duplicates(subset=['icao'],keep='first')

    return new_aircraft, operator, countries, airports

def insert_tables(aircraft, operator, countries, airports):
    conn = create_postgres_conn()

    data = [countries, airports, operator, aircraft]
    table_names = ['Country', 'Airport', 'Operator', 'Aircraft']
    for table_name, df in zip(table_names, data):
        print(f'Inserting {table_name}...')
        with conn.cursor() as cursor:     
            columns = df.columns.tolist()
            values = [tuple(row) for row in df.values]
            insert_sql = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES %s"
            execute_values(cursor, insert_sql, values)
            conn.commit()
    conn.close()
    print('Done.')

def main():
    aircraft, operator, countries, airports = get_tables()
    insert_tables(aircraft, operator, countries, airports)

if __name__ == '__main__':
    main()