from fastapi import FastAPI, APIRouter, Depends, Request
from fastapi.responses import JSONResponse
import uvicorn
from pydantic import BaseModel, Field
from starlette.middleware.base import BaseHTTPMiddleware

from src.config import s3_bucket
from src.middlewares.file_upload_middleware import file_upload_middleware

class Item(BaseModel):
  description: str | None = Field(
        default=None, title="The description of the item", max_length=300
    )

app = FastAPI(title="Audio Extractor")

router = APIRouter()
audio_router = APIRouter(prefix="/audio", dependencies=[Depends(file_upload_middleware)])

@router.get("/health")
def check_health():
  return { "success": True }



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


if __name__ == "__main__":
  uvicorn.run("src.main:app", host="0.0.0.0", port=8000, log_level="info", reload=True)