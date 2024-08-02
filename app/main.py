from fastapi import FastAPI, HTTPException
from pymongo import MongoClient
from pydantic import BaseModel
from redis import Redis
from typing import List
import os

app = FastAPI()
client = MongoClient(os.getenv("MONGODB_URI"))
db = client.messages_db


class Message(BaseModel):
    username: str
    text: str


@app.get("/api/v1/messages", response_model=List[Message])
async def get_messages():
    messages = list(db.messages.find())
    return messages


@app.post("/api/v1/message")
async def create_message(message: Message):
    db.messages.insert_one(message.model_dump())
    return {"status": "message created", "message_data": message}
