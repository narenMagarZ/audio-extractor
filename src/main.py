from fastapi import FastAPI, APIRouter, Depends, Request
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import signal
from datetime import datetime as DateTime, timezone
import asyncio

from src.middlewares.file_upload_middleware import file_upload_middleware
from src.database import database
from src.producer import MessageProducer
from src.consumer import MessageConsumer
from src.logger import Logger
from src.services.audio_extraction_job_service import AudioExtractionJobService



message_producer = MessageProducer()
message_consumer = MessageConsumer()


@asynccontextmanager
async def lifespan(app: FastAPI):
  database.connect()
  await message_producer.connect()
  await message_consumer.connect()
  asyncio.create_task(message_consumer.consume())
  Logger().info("Rabbitmq connected successfully")
  yield
  await MessageProducer.close()
  await MessageConsumer.close()

app = FastAPI(title="Audio Extractor", lifespan=lifespan)


router = APIRouter()
audio_router = APIRouter(prefix="/audio", dependencies=[Depends(file_upload_middleware)])

@router.get("/health")
def check_health():
  return JSONResponse(status_code=200, content={ "success": True })

@audio_router.post("/extract/{req_id}")
async def extract_audio(request: Request):
  object_key = request.file.get("key")
  pending_extraction_job = AudioExtractionJobService().create({
    "meta": { 
      "key": object_key, 
      "filename": request.file.get("filename"),
      "media_type": request.file.get("content-type"),
      "size": request.file.get("size") # in bytes
    }, 
    "status": "initiated", 
    "triggered_at": DateTime.now(timezone.utc)
  })
  await message_producer.publish({"key": object_key, "job_id": pending_extraction_job.id})
  return { "success": True }

router.include_router(audio_router)
app.include_router(router, prefix="/api/v1")

@app.exception_handler(Exception)
async def generic_exception_handler(request, exc):
  return JSONResponse(
    status_code=500,
    content={
      "success": False,
      "error": "Internal server error",
      "detail": str(exc)
    }
  )



def handle_shutdown():
  print("Server shutdown...")

signal.signal(signal.SIGINT, handle_shutdown)
signal.signal(signal.SIGTERM, handle_shutdown)

