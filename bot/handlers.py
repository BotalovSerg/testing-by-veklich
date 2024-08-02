from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext

from config_database import db
from states import AddMessageSG

router = Router()


@router.message(Command("start"))
async def send_start(message: Message):
    await message.answer(
        "Welcome! Use /getmessages to see all messages.\n Use /create to create new message."
    )


@router.message(StateFilter(None), Command("getmessages"))
async def get_messages(message: Message):
    messages = list(db.messages.find())
    response = "\n".join(f"{msg['username']}: {msg['text']}" for msg in messages)
    await message.answer(response or "No messages found.")


@router.message(StateFilter(None), Command("create"))
async def create_message(message: Message, state: FSMContext):
    await state.set_state(AddMessageSG.username)
    await message.answer("Message creation mode, write your username")


@router.message(AddMessageSG.username, F.text)
async def stare_save_username(message: Message, state: FSMContext):
    await state.update_data(username=message.text)
    await state.set_state(AddMessageSG.text)

    await message.answer("Write a message")


@router.message(AddMessageSG.text, F.text)
async def state_save_text(message: Message, state: FSMContext):
    await state.update_data(text=message.text)
    data = await state.get_data()
    await state.clear()

    db.messages.insert_one(data)

    await message.answer("Message created")
