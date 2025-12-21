from src.database import database
from src.models.audio_extraction_job_model import AudioExtractionJobModel

class BaseRepository:
  def __init__(self, model):
    self.model = model

  def find_by_pk(self, id: int):
    database.db.query(self.model).filter_by(id=id)

  def insert(self, data):
    database.db.add(data)
    database.db.commit()
    database.db.refresh(data)
    return data

  def update_one(self, id: int, data: dict):
    database.db.query(self.model).filter(self.model.id == id).update(data)
    database.db.commit()
    return

  def delete(self, where):
    pass