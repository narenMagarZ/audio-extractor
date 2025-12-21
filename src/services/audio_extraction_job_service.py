from src.repositories.audio_extraction_job_repository import AudioExtractionJobRepository
from src.models.audio_extraction_job_model import AudioExtractionJobModel

class AudioExtractionJobService:
  __repository: AudioExtractionJobRepository
  def __init__(self):
    self.__repository = AudioExtractionJobRepository()

  def create(self, data):
    job = AudioExtractionJobModel(triggered_at=data["triggered_at"], status=data["status"], meta=data["meta"])
    return self.__repository.insert(job)
 
  def update_one(self, id, data: dict):
    self.__repository.update_one(id, data)