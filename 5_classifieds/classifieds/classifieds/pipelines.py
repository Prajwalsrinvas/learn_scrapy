# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import hashlib
import json

import boto3
import psycopg2
import pymongo
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem


class ClassifiedsRemoveDuplicateTitlesPipeline:
    def __init__(self):
        self.titles_seen = set()

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        title = adapter.get("title")
        if title in self.titles_seen:
            raise DropItem(f"ad with duplicate title: {item}")
        else:
            self.titles_seen.add(title)
            return item


class ClassifiedsRemoveMissingPhoneNumbersPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if (not adapter.get("mobile")) and (not adapter.get("landline")):
            raise DropItem(f"ad with no contact number: {item}")
        else:
            return item


class MongoPipeline:
    collection_name = "classifieds"

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get("MONGO_URI"),
            mongo_db=crawler.settings.get("MONGO_DATABASE"),
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.db[self.collection_name].insert_one(ItemAdapter(item).asdict())
        return item


class PostgresPipeline:
    def __init__(self, postgres_settings):
        self.postgres_settings = postgres_settings

    @classmethod
    def from_crawler(cls, crawler):
        postgres_settings = {
            "host": crawler.settings.get("POSTGRES_HOST"),
            "port": crawler.settings.get("POSTGRES_PORT"),
            "database": crawler.settings.get("POSTGRES_DATABASE"),
            "user": crawler.settings.get("POSTGRES_USER"),
            "password": crawler.settings.get("POSTGRES_PASSWORD"),
        }
        return cls(postgres_settings)

    def open_spider(self, spider):
        self.database = self.postgres_settings["database"]
        self.connection = psycopg2.connect(**self.postgres_settings)
        self.cursor = self.connection.cursor()
        # Check if the database already exists
        self.cursor.execute(
            "SELECT 1 FROM pg_database WHERE datname = %s", (self.database,)
        )
        exists = self.cursor.fetchone()

        if not exists:
            # Create the new database
            self.cursor.execute(f"CREATE DATABASE {self.database}")
            print(f"Database '{self.database}' created successfully.")
        else:
            print(f"Database '{self.database}' already exists.")
        # Define the SQL query to create the schema if it doesn't exist
        create_schema_query = f"""
            CREATE SCHEMA IF NOT EXISTS {self.database};
        """

        # Execute the query
        self.cursor.execute(create_schema_query)
        self.cursor.execute(
            f"""
            CREATE TABLE IF NOT EXISTS {self.database}.classifieds(
                id SERIAL PRIMARY KEY,
                title TEXT,
                locality TEXT,
                address TEXT,
                landline TEXT,
                mobile TEXT,
                price TEXT
            )"""
        )

    def close_spider(self, spider):
        self.connection.close()

    def process_item(self, item, spider):
        # Assuming you have a table named 'your_table' with the appropriate columns
        # Adjust the SQL query and table structure based on your needs
        adapter = ItemAdapter(item)
        self.cursor.execute(
            f"""INSERT INTO {self.database}.classifieds (title,locality,address,landline,mobile,price) VALUES (%s,%s,%s,%s,%s,%s)""",
            (
                adapter.get("title"),
                adapter.get("locality"),
                adapter.get("address"),
                adapter.get("landline"),
                adapter.get("mobile"),
                adapter.get("price"),
            ),
        )

        self.connection.commit()

        return item


class UploadToS3Pipeline:
    def __init__(self, bucket):
        self.bucket = bucket

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            bucket=crawler.settings.get("S3_BUCKET"),
        )

    def process_item(self, item, spider):
        s3_client = boto3.client("s3")
        item_bytes = json.dumps(ItemAdapter(item).asdict())
        item_key = hashlib.md5(item_bytes.encode()).hexdigest()
        s3_client.put_object(
            Body=item_bytes, Bucket=self.bucket, Key=f"{item_key}.json"
        )
        return item
