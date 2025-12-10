from src.database import database

class BaseRepository:
  def __init__(self, model):
    self.model = model

  def find_by_pk(self, id: int):
    database.db.query(self.model).filter_by(id=id)

  def insert(self, data: any):
    database.db.add(data)
    database.db.commit()

  def update(self, values: dict, where: any):
    pass

  def delete(self, where: any):
    pass