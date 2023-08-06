import os
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

db_username = os.getenv('DATABASE_USERNAME', 'SA')
db_password = os.getenv('DATABASE_PASSWORD', 'cas-dev.Local')
db_host = os.getenv('DATABASE_HOST', 'localhost')
db_name = os.getenv('DATABASE_NAME', 'acabim_common')

db_url = f'mssql+pyodbc://{db_username}:{db_password}@{db_host}/{db_name}?driver=ODBC+Driver+17+for+SQL+Server'

sql_engine = create_engine(db_url, echo=True)
Session = sessionmaker(bind=sql_engine)
