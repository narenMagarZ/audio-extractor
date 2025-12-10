from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import sessionmaker
from src.config import db

class Database:
  __engine: Engine
  __pg_url: str = f"postgresql://{db.get("db_username")}:{db.get("db_password")}@{db.get("db_host")}/{db.get("db_name")}"
  __db: sessionmaker

  def __init__(self):
    self.__create_engine()
    self.__db = sessionmaker(
      bind=self.__engine, 
      autocommit=False,
      autoflush=False,
      expire_on_commit=False
    )


  def __create_engine(self):
    self.__engine = create_engine(self.__pg_url, echo=True, pool_size=100)

  def close(self):
    self.__db.close_all()

