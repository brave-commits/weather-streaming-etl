from urllib.parse import quote_plus
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import pandas as pd
from config.config import ParamsFactory

params = ParamsFactory.create_params()


class BaseDBConn:
    def __init__(self, server, database, driver, username, password):
        self.server = server
        self.database = database
        self.driver = driver
        self.username = username,
        self.password = password
        self.conn_string = f"DRIVER={self.driver};SERVER={self.server};DATABASE={self.database};UID=sa;PWD={self.password};TrustServerCertificate=yes"
        self.params = quote_plus(self.conn_string)
        self.engine = create_engine(f"mssql+pyodbc:///?odbc_connect={self.params}", fast_executemany=True)
        self.connection = self.engine.connect().execution_options(stream_results=True)


class DBSession(BaseDBConn):
    def __init__(self, server, database, driver, username, password):
        super().__init__(server, database, driver, username, password)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    @classmethod
    def create_session_dst(cls):
        db_session_dst = cls(params.db_server, params.db_database, params.db_driver, params.db_usr, params.db_pwd)
        return db_session_dst

    @classmethod
    def df_to_sql(cls, df):
        session = cls(params.db_server, params.db_database, params.db_driver, params.db_usr, params.db_pwd).session
        df.to_sql(name=params.db_table, schema=params.db_schema, con=session.bind, if_exists='replace', index=True)


Base = declarative_base()


class DynamicTable(Base):
    __tablename__ = 'COLUMNS'
    __table_args__ = {'schema': 'INFORMATION_SCHEMA'}
    TABLE_NAME = Column(String)
    TABLE_SCHEMA = Column(String)
    COLUMN_NAME = Column(String, primary_key=True)
    IS_NULLABLE = Column(String)
    DATA_TYPE = Column(String)

    @classmethod
    def source_attr(cls, table, schema):
        dbsession = DBSession.create_session_src()
        session = dbsession.session
        query = session.query(DynamicTable). \
            filter(DynamicTable.TABLE_NAME.like(table)). \
            filter(DynamicTable.TABLE_SCHEMA.like(schema))
        results = query.all()

        data_for_dataframe = []
        for r in results:
            row_data = {
                'TABLE_NAME': r.TABLE_NAME,
                'TABLE_SCHEMA': r.TABLE_SCHEMA,
                'COLUMN_NAME': r.COLUMN_NAME,
                'IS_NULLABLE': r.IS_NULLABLE,
                'DATA_TYPE': r.DATA_TYPE,
            }
            data_for_dataframe.append(row_data)

        df = pd.DataFrame(data_for_dataframe)
        session.close()
        return df

    @classmethod
    def create_table_class(cls, table, schema):
        df = DynamicTable.source_attr(table, schema)
        class_name = f"{table.title()}TableClass"
        attributes = {
            col: Column(String) for col in df['COLUMN_NAME']
        }
        attributes['Id'] = Column(Integer, primary_key=True)
        attributes['__tablename__'] = table
        attributes['__table_args__'] = {'schema': schema}

        return type(class_name, (Base,), attributes)