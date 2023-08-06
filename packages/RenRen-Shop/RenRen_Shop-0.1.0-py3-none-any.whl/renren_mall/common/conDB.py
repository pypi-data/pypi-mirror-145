import pymysql
from sqlalchemy import create_engine


class connection_db(object):
    def __init__(self,host,database,user,password):
        self.host = host
        self.database = database
        self.user = user
        self.password = password

    def con(self):
        con = create_engine(f'mysql+pymysql://{self.user}:{self.password}@{self.host}:3306/{self.database}')
        return con

    def db(self):
        db = pymysql.connect(host=self.host, database=self.database, user=self.user, password=self.password)
        return db
