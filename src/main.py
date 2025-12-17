from fastapi import FastAPI, APIRouter, Depends, Request
from fastapi.responses import JSONResponse
import signal
import threading

from src.middlewares.file_upload_middleware import file_upload_middleware
from src.database import database
from src.message_producer.producer import message_producer, message_consumer

database.connect()
message_consumer.consume()

app = FastAPI(title="Audio Extractor")

router = APIRouter()
audio_router = APIRouter(prefix="/audio", dependencies=[Depends(file_upload_middleware)])

@router.get("/health")
def check_health():
  return JSONResponse(status_code=200, content={ "success": True })

@audio_router.post("/extract/{req_id}")
async def extract_audio(request: Request):
  print(request.file, 'request.file')
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

def sleep_server():
  message_producer.produce({"name": "naren"})
  print('produced')
timer = threading.Timer(5, sleep_server)
timer.start()