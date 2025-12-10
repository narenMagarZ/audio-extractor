from sqlalchemy import Column, Integer, String, DateTime, Text, Enum, JSON, func


from src.models.base_model import BaseModel

class AudioExtractionJobModel(BaseModel):
  __tablename__ = "audio_extraction_jobs"

  id = Column(Integer, primary_key=True, index=True, nullable=False)
  triggered_at = Column(DateTime, nullable=False)
  completed_at = Column(DateTime, nullable=True)
  status = Column(String, nullable=False)
  failed_reason = Column(Text, nullable=True)
  meta = Column(JSON, nullable=True)
  created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
  updated_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
  deleted_at = Column(DateTime(timezone=True), nullable=True)