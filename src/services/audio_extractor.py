import moviepy
import aioboto3


from src.config import s3_bucket

class S3Helper:
    __session: aioboto3.Session

    def __init__(self):
        self.__session = aioboto3.Session(
            aws_access_key_id=s3_bucket.get('access_key'),
            aws_secret_access_key=s3_bucket.get('secret_key'),
            region_name=s3_bucket.get('s3_region')
        )

    async def get_object(self, key: str):
        async with self.__session.client('s3') as s3:
            response = await s3.get_object(Bucket=s3_bucket.get("bucket"), Key=key)
            content = response['Body'].read()
            return content
        
    async def head_object(self, key: str):
        async with self.__session.client('s3') as s3:
            metadata = await s3.head_object(Bucket=s3_bucket.get("bucket"), Key=key)
            print(metadata)
        return metadata
            

class AudioExtractor:
    def __init__(self):
        pass


    def extract(self, key: str):
        print(key, 'key')
        # metadata = S3Helper().head_object(key)
        # S3Helper().get_object(key)
        return