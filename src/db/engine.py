from src.env_reader import USERNAME, PASSWORD, DATABASE, HOST, PORT
from sqlalchemy import URL
from sqlalchemy import create_engine

url = URL.create(
        drivername='postgresql+psycopg2',
        username=USERNAME,
        password=PASSWORD,
        database=DATABASE,
        host=HOST,
        port=int(PORT)
    )

engine = create_engine(url)
