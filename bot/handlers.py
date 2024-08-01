from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from config_database import db

router = Router()


@router.message(Command("start"))
async def send_start(message: Message):
    await message.reply("Welcome! Use /getmessages to see all messages.")


@router.message(Command("getmessages"))
async def get_messages(message: Message):
    messages = list(db.messages.find())
    response = '\n'.join(f"{msg['username']}: {msg['text']}" for msg in messages)
    await message.reply(response or "No messages found.")


@router.message(Command("create"))
async def create_message(message: Message):
    await message.reply("Send me your username and message like 'username: Your message'.")
