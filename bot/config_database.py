import os

from pymongo import MongoClient
from redis import Redis

client = MongoClient(os.getenv("MONGODB_URI"))
db = client.messages_db
redis_client = Redis(host=os.getenv("REDIS_HOST"))
