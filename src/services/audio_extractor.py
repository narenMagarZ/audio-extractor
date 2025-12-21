import aioboto3
import aiofiles
from moviepy import VideoFileClip
import os
from datetime import datetime as Datetime, timezone

from src.config import s3_bucket
from src.services.audio_extraction_job_service import AudioExtractionJobService
from src.logger import Logger

class S3Helper:
    __session: aioboto3.Session

    def __init__(self):
        self.__session = aioboto3.Session(
            aws_access_key_id=s3_bucket.get('access_key'),
            aws_secret_access_key=s3_bucket.get('secret_key'),
            region_name=s3_bucket.get('s3_region')
        )

    async def get_object(self, key: str):
        temp_path = f"public/{key}.mp4"
        async with self.__session.client('s3') as s3:
            os.makedirs(os.path.dirname(temp_path), exist_ok=True)
            response = await s3.get_object(Bucket=s3_bucket.get("bucket"), Key=key)
            async with aiofiles.open(temp_path, "wb") as f:
                async for chunk in response["Body"].iter_chunks():
                    await f.write(chunk)
        return temp_path
        
    async def head_object(self, key: str):
        async with self.__session.client('s3') as s3:
            metadata = await s3.head_object(Bucket=s3_bucket.get("bucket"), Key=key)
        return metadata
    
    async def put_file_object(self, key: str, path: str):
        async with self.__session.client('s3') as s3:
            async with aiofiles.open(path, "rb") as f:
                await s3.upload_fileobj(
                    f,
                    s3_bucket.get("bucket"),
                    key,
                    ExtraArgs={'ContentType': "audio/mpeg"}
                )
            

class AudioExtractor:
    def __init__(self):
        pass

    async def extract(self, data):
        job_id = data['job_id']
        object_key = data['key']
        AudioExtractionJobService().update_one(job_id, { "status": "pending" })
        s3_helper = S3Helper()
        await s3_helper.head_object(object_key)
        video_path = await s3_helper.get_object(object_key)

        audio_object_key = f"{object_key}.mp3".replace("video", "audio", 1)
        audio_file_path = f"public/{object_key}.mp3".replace("video", "audio", 1)

        clip = VideoFileClip(video_path)
        os.makedirs(os.path.dirname(audio_file_path), exist_ok=True)
        clip.audio.write_audiofile(audio_file_path, logger=None)
        clip.close()
        
        await s3_helper.put_file_object(audio_object_key, audio_file_path)
        AudioExtractionJobService().update_one(job_id, { "status": "completed", "completed_at": Datetime.now(timezone.utc) })
        Logger().info("Audio extraction job completed...")
    