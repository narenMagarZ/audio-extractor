from src.database import DbEngine
from src.models import base_model, audio_extraction_job_model


print("Creating table audio_extraction_jobs...")
base_model.BaseModel.metadata.create_all(bind=DbEngine().engine)
print("Completed...")
