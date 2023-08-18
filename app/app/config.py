from sqlalchemy import create_engine, Column, Integer, String, DateTime, text, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from sqlalchemy import MetaData
from sqlalchemy import Table, Column, Integer, String



class SQLServerConnector:
    def __init__(self, username, password, server, database):
        self.connection_string = f'mssql+pyodbc://{username}:{password}@{server}/{database}?driver=ODBC+Driver+17+for+SQL+Server'
        self.engine = create_engine(self.connection_string, echo=False, pool_pre_ping=True, pool_size=20, max_overflow=5)
        self.Base = declarative_base()
        self.Session = sessionmaker(bind=self.engine, autoflush=False, autocommit=False)

    def create_table(self, model_class):
        self.Base.metadata.create_all(self.engine)

    def insert_data(self, model_instance):
        with self.Session() as session:
            session.add(model_instance)
            session.commit()

    def query_data(self, model_class, filter_conditions=None, batch_size=1000):
        with self.Session() as session:
            query = session.query(model_class)
            if filter_conditions:
                query = query.filter_by(**filter_conditions)
            offset = 0
            while True:
                batch = query.limit(batch_size).offset(offset).all()
                if not batch:
                    break
                for item in batch:
                    yield item
                offset += batch_size




