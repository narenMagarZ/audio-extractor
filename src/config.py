import os 

import dotenv

dotenv.load_dotenv()

s3_bucket = {
  "bucket": os.getenv("S3_BUCKET_NAME"),
  "access_key": os.getenv("S3_BUCKET_ACCESS_KEY"),
  "secret_key": os.getenv("S3_BUCKET_SECRET_KEY"),
  "s3_region": os.getenv("S3_BUCKET_REGION")
}


db = {
  "db_host": os.getenv("DB_HOST"),
  "db_username": os.getenv("DB_USER"),
  "db_port": os.getenv("DB_PORT"),
  "db_name": os.getenv("DB_NAME"),
  "db_password": os.getenv("DB_PASSWORD")
}