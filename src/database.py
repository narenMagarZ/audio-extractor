from threading import Lock

from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import sessionmaker, Session

from src.config import db

class SingletonMeta(type):
  _instance = None
  _lock: Lock = Lock()
    
  def __call__(self, *args, **kargs):
    with self._lock:
      if self._instance is None:
        self._instance = super().__call__(*args, **kargs)
    return self._instance

class DbEngine:
  __pg_url: str = f"postgresql://{db.get("db_username")}:{db.get("db_password")}@{db.get("db_host")}/{db.get("db_name")}"

  def __init__(self):
    self.__engine = create_engine(self.__pg_url, echo=True, pool_size=100)

  @property
  def engine(self):
    return self.__engine

class Database(metaclass=SingletonMeta):
  __engine: Engine
  __pg_url: str = f"postgresql://{db.get("db_username")}:{db.get("db_password")}@{db.get("db_host")}/{db.get("db_name")}"
  db: Session

  def __init__(self):
    pass

  def connect(self):
    try:
      self.__engine = create_engine(self.__pg_url, echo=True, pool_size=100)
      self.db = sessionmaker(
        bind=self.__engine, 
        autocommit=False,
        autoflush=False,
        expire_on_commit=False
      )()
    except Exception as e:
      print("Error connecting to DB", e)
      raise e

  def close(self):
    self.__db.close_all()

database = Database()