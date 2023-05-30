import datetime
import logging
import requests
import azure.functions as func
import os
from dotenv import load_dotenv
import boto3
import json
import pandas as pd
import io
import time

load_dotenv()

def main(mytimer: func.TimerRequest) -> None:
    utc_timestamp = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()

    logging.info(f"Timer function executed at: {utc_timestamp}")

    # Make GET request to the API
    users = [os.environ['OPEN_SKY_USERNAME_1'],os.environ['OPEN_SKY_USERNAME_5']]
    passwords = [os.environ['OPEN_SKY_PASSWORD_1'],os.environ['OPEN_SKY_PASSWORD_5']]

    # session = requests.Session()
    # session.auth = (user, password)
    for u, p in zip(users, passwords):
        response = requests.get("https://opensky-network.org/api/states/all",auth=(u, p))
        if response.status_code == 200:
            # Process the response if needed
            response_body = response.json()
            logging.info(f"API request success with status code: 200")
            break
        elif response.status_code == 429:
            logging.error(f"API request failed with status code: 429")
            pass
        else:
            logging.error(f"API request failed with status code: {response.status_code}")
            response_body = None
            break

    if response_body:
        decoded = json.loads(response.text)

        response = requests.request("PUT","http://35.176.80.148/states",json=decoded['states'],timeout=15)
        if response.status_code == 200:
            logging.info(f"{response.status_code}: States data sent successfully")
        else:
            logging.error(f"{response.status_code}: States failed to be sent to web server.")

        columns = ["icao24", "callsign","origin_country",
                "time_position","last_contact","longitude",
                "latitude","baro_altitude","on_ground",
                "velocity","true_track","vertical_rate",
                "sensors","geo_altitude","squawk",
                "spi","position_source"]
        
        df = pd.DataFrame(decoded['states'],columns=columns).drop(["sensors",'squawk','spi','position_source','time_position'],axis=1)

        bucket_name='opensky-state-bucket'
        s3_client = boto3.client('s3',aws_access_key_id=os.environ['AWS_ACCESS_KEY'], aws_secret_access_key=os.environ['SECRET_ACCESS_KEY'])

        out_buffer = io.BytesIO()
        df.to_parquet(out_buffer, index=False)

        s3_client.put_object(Bucket=bucket_name, Key=f'{int(time.time())}.parquet', Body=out_buffer.getvalue())