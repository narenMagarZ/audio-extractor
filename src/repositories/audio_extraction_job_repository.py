from src.repositories.base_repository import BaseRepository
from src.models.audio_extraction_job_model import AudioExtractionJobModel

class AudioExtractionJobRepository(BaseRepository):
  def __init__(self):
    super().__init__(AudioExtractionJobModel)