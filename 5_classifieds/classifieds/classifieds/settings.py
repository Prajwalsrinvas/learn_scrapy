import os

import hvac
from dotenv import load_dotenv

load_dotenv()


BOT_NAME = "classifieds"

SPIDER_MODULES = ["classifieds.spiders"]
NEWSPIDER_MODULE = "classifieds.spiders"


# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

ITEM_PIPELINES = {
    "classifieds.pipelines.ClassifiedsRemoveDuplicateTitlesPipeline": 300,
    "classifieds.pipelines.ClassifiedsRemoveMissingPhoneNumbersPipeline": 400,
    "classifieds.pipelines.MongoPipeline": 500,
    "classifieds.pipelines.PostgresPipeline": 600,
    "classifieds.pipelines.UploadToS3Pipeline": 600,
}


DOWNLOAD_HANDLERS = {
    "http": "scrapy_impersonate.ImpersonateDownloadHandler",
    "https": "scrapy_impersonate.ImpersonateDownloadHandler",
}

TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
HTTPCACHE_ENABLED = True

# dotenv or vault
SECRETS_LOCATION = "dotenv"

if SECRETS_LOCATION == "dotenv":
    MONGO_URI = os.getenv("MONGO_URI")
    MONGO_DATABASE = os.getenv("MONGO_DATABASE")

    POSTGRES_HOST = os.getenv("POSTGRES_HOST")
    POSTGRES_PORT = os.getenv("POSTGRES_PORT")
    POSTGRES_DATABASE = os.getenv("POSTGRES_DATABASE")
    POSTGRES_USER = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")

    S3_BUCKET = os.getenv("S3_BUCKET")

elif SECRETS_LOCATION == "vault":
    client = hvac.Client(
        url="http://127.0.0.1:8200", token=os.getenv("VAULT_ROOT_TOKEN")
    )

    mongo_secrets = client.secrets.kv.read_secret_version("mongo")["data"]["data"]
    postgres_secrets = client.secrets.kv.read_secret_version("postgres")["data"]["data"]
    s3_secrets = client.secrets.kv.read_secret_version("s3")["data"]["data"]

    MONGO_URI = mongo_secrets["MONGO_URI"]
    MONGO_DATABASE = mongo_secrets["MONGO_DATABASE"]

    POSTGRES_HOST = postgres_secrets["POSTGRES_HOST"]
    POSTGRES_PORT = postgres_secrets["POSTGRES_PORT"]
    POSTGRES_DATABASE = postgres_secrets["POSTGRES_DATABASE"]
    POSTGRES_USER = postgres_secrets["POSTGRES_USER"]
    POSTGRES_PASSWORD = postgres_secrets["POSTGRES_PASSWORD"]

    S3_BUCKET = s3_secrets["S3_BUCKET"]

LOG_LEVEL = "INFO"
