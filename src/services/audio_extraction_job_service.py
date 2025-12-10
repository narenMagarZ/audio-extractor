from src.repositories.audio_extraction_job_repository import AudioExtractionJobRepository

class AudioExtractionJobService:
  _repository: AudioExtractionJobRepository
  def create(self):
    
    self._repository.insert()

  def update_one(self):
    self._repository.update()

    
