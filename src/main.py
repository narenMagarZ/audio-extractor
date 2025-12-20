from fastapi import FastAPI, APIRouter, Depends, Request
from fastapi.responses import JSONResponse
import signal
import threading

from src.middlewares.file_upload_middleware import file_upload_middleware
from src.database import database
from src.producer import message_producer
from src.consumer import MessageConsumer
from src.logger import Logger

database.connect()

try:
  threads = []
  threads.append(threading.Thread(target=message_producer.connect))
  threads.append(threading.Thread(target=MessageConsumer().consume))

  for thread in threads:
    thread.start()
  Logger().info("Rabbitmq started successfully...")
except Exception as e:
  raise



app = FastAPI(title="Audio Extractor")

router = APIRouter()
audio_router = APIRouter(prefix="/audio", dependencies=[Depends(file_upload_middleware)])

@router.get("/health")
def check_health():
  return JSONResponse(status_code=200, content={ "success": True })

@audio_router.post("/extract/{req_id}")
async def extract_audio(request: Request):
  print(request.file, 'request.file')
  # create job
  # start job
  # return
  message_producer.produce(request.file)
  # consumer listening job
  # process job
  # end job
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

