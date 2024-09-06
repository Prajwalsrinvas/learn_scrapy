import os

from dotenv import load_dotenv

load_dotenv()

BOT_NAME = "free_images"

SPIDER_MODULES = ["free_images.spiders"]
NEWSPIDER_MODULE = "free_images.spiders"


ROBOTSTXT_OBEY = True


ITEM_PIPELINES = {"scrapy.pipelines.images.ImagesPipeline": 1}

IMAGES_THUMBS = {"small": (50, 50), "big": (270, 270)}
# SET THIS TO REQUIRED IMAGES DESTINATION
# options: local, ftp, minio_s3, aws_s3
# for ftp: run ftp_server.py
# for minio_s3: run ./start_minio_server.sh, create bucket: http://192.168.29.23:9001/browser/add-bucket
STORE = "aws_s3"

if STORE == "local":
    # Local Folder
    # https://docs.scrapy.org/en/latest/topics/media-pipeline.html#file-system-storage
    IMAGES_STORE = "images"
elif STORE == "ftp":
    # FTP
    # https://docs.scrapy.org/en/latest/topics/media-pipeline.html#ftp-server-storage
    IMAGES_STORE = (
        f"ftp://{os.getenv('FTP_USERNAME')}:{os.getenv('FTP_PASSWORD')}@localhost:2121"
    )
elif STORE == "minio_s3":
    # S3
    # https://docs.scrapy.org/en/latest/topics/media-pipeline.html#amazon-s3-storage
    IMAGES_STORE = "s3://scrapy-images-bucket/"  # trailing slash required
    AWS_ENDPOINT_URL = "http://127.0.0.1:9000"

    AWS_ACCESS_KEY_ID = os.getenv("MINIO_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.getenv("MINIO_SECRET_ACCESS_KEY")
    AWS_USE_SSL = False
    AWS_VERIFY = False
elif STORE == "aws_s3":
    IMAGES_STORE = "s3://scrapy-images-bucket/"  # trailing slash required

    AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")


HTTPCACHE_ENABLED = True
