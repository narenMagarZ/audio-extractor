from fastapi import FastAPI, APIRouter, Depends, Request
from fastapi.responses import JSONResponse

from src.middlewares.file_upload_middleware import file_upload_middleware
from src.database import database

database.connect()

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