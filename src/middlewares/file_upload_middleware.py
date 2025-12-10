from fastapi import UploadFile, File, Request
import aioboto3

from src.config import s3_bucket

async def file_upload_middleware(request: Request, req_id: str, file: UploadFile = File(...)):
  try:
    session = aioboto3.Session(
      aws_access_key_id=s3_bucket.get('access_key'),
      aws_secret_access_key=s3_bucket.get('secret_key'),
      region_name=s3_bucket.get('s3_region')
    )
    async with session.client('s3') as s3:
      bucket_key = f"{req_id}"
      await s3.upload_fileobj(
        file.file,
        s3_bucket.get("bucket"),
        bucket_key,
        ExtraArgs={'ContentType': file.content_type}
      )
      request.file = {
        "file": file,
        "key": bucket_key
      }
  except Exception as error:
    raise error