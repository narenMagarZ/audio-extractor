from sqlalchemy import Column, Integer, DateTime, Text, Enum, JSON, func, String

from src.models.base_model import BaseModel

class Audio_Extraction_Job_Enum(Enum):
  initiated = "initiated"
  failed = "failed"
  completed = "completed"

class AudioExtractionJobModel(BaseModel):
  __tablename__ = "audio_extraction_jobs"

  id = Column(Integer, primary_key=True, index=True, nullable=False)
  triggered_at = Column(DateTime(timezone=True), nullable=False)
  completed_at = Column(DateTime(timezone=True), nullable=True)
  status = Column(String, nullable=False)
  failed_reason = Column(Text, nullable=True)
  meta = Column(JSON, nullable=True)
  created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
  updated_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
  deleted_at = Column(DateTime(timezone=True), nullable=True)