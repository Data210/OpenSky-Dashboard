import configparser
import os
from dotenv import load_dotenv

load_dotenv()


def create_connection_string():

    # READ FROM ENV
    driver = os.getenv("DB_DRIVER")
    server = os.getenv("DB_SERVER")
    port = os.getenv("DB_PORT")
    database_name = os.getenv("DB_NAME")
    dialect = os.getenv("DB_DIALECT")
    db_password = os.getenv("DB_PASSWORD")
    db_username = os.getenv("DB_USERNAME")
    
    connection_string = f"{dialect}://{db_username}:{db_password}@{server}:{port}/{database_name}?driver={driver}"
    return connection_string
