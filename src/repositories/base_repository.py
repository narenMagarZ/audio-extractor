from sqlalchemy import insert, update, delete, select

class BaseRepository:
  def __init__(self, model):
    self.model = model

  def find_by_pk(self, id: int):
    select(self.model).where(id)

  def insert(self, values: dict):
    insert(self.model).values(values)

  def update(self, values: dict, where: any):
    update(self.model).values(values).where(where)

  def delete(self, where: any):
    delete(self.model).where(where)