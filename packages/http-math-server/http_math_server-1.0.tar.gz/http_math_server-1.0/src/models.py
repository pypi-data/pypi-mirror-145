import sqlalchemy as sa

from typing import List

from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.engine.base import Engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_utils import database_exists, create_database


Base = declarative_base()
metadata = Base.metadata


class DataModel(Base):
    __tablename__ = 'expression_data'

    id = sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True)
    operator = sa.Column('operator', sa.String(10))
    num1 = sa.Column('num1', sa.Numeric())
    num2 = sa.Column('num2', sa.Numeric())
    result = sa.Column('result', sa.Numeric())


    def to_dict(self) -> dict:
        return {
            'operator': self.operator,
            'num1': self.num1,
            'num2': self.num2,
            'result': self.result,
        }


class UserDatabaseInterfase:

    def __init__(self, user: str, passwd: str, host: str, port: int, db_name: str):
        self.__user = user
        self.__passwd = passwd
        self.__host = host
        self.__port = port
        self.__db_name = db_name
        self.__engine = self.__get_engine()

        self.__session = Session(bind=self.__engine)


    def __get_engine(self) -> Engine:
        url = f"postgresql://{self.__user}:{self.__passwd}@{self.__host}:{self.__port}/{self.__db_name}"
        if not database_exists(url):
            create_database(url)
        return create_engine(url)


    def insert_data(self, data: dict):
        new_data = DataModel(
            operator = data['operator'],
            num1 = data['num1'],
            num2 = data['num2'],
            result = data['result']    
        )

        self.__session.add(new_data)
        self.__session.commit()


    def get_data(self, op='', limit=0, offset=0) -> List[dict]:
        if op:
            data = self.__session.query(DataModel).filter(DataModel.operator == op)
        else:
            data = self.__session.query(DataModel)
            
        if limit > 0:
            data = data.limit(limit)
        if offset > 0:
            data = data.offset(offset)

        return [item.to_dict() for item in data.all()]


    def create_database(self):
        engine = self.__get_engine()
        metadata.create_all(engine)


    def drop_table(self):
        DataModel.__table__.drop(self.__engine)
