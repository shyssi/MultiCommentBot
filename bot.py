import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message, MessageEntity, FSInputFile
from aiogram.types import LinkPreviewOptions
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandObject
from environs import Env
from datetime import datetime, timezone
import psutil
import json

env = Env()
env.read_env("tokens.env")
TOKEN_TG = env.str("TOKEN")
IMAGE_DIR = "static"
START_TIME = datetime.now(timezone.utc)

telegram_bot = Bot(token=TOKEN_TG)
dp = Dispatcher()

with open('config.json', 'r', encoding='utf-8') as f:
    CONFIG = json.load(f)
    ID_CHANNEL = [int(id) for id in CONFIG]
    print("Конфиг загружен!")
    print(f"ID каналов:{ID_CHANNEL}")


async def data_message(message):
    chat_id = str(message.chat.id)
    channel_id = str(message.sender_chat.id) if message.sender_chat else message.from_user.id
    return chat_id, channel_id


async def message_post(chat_id, message, file_path, caption, keyboard=None):
    print(file_path)
    file = FSInputFile(file_path)

    kwargs = {
        "caption": caption,
        "reply_to_message_id": message.message_id,
        "reply_markup": keyboard,
        "parse_mode": ParseMode.HTML,
    }
    try:
        if file_path == "static/None":
            kwargs = {
                    "text": caption,
                    "reply_to_message_id": message.message_id,
                    "reply_markup": keyboard,
                    "parse_mode": ParseMode.HTML,
                    "link_preview_options": LinkPreviewOptions(is_disabled=True)
                }
            await telegram_bot.send_message(chat_id, **kwargs)
        else:
            await telegram_bot.send_photo(chat_id, file, **kwargs)
    except Exception as e:
        print(f"Error: {e}")


@dp.message(Command("status"))
async def status_bot(message: Message, command: CommandObject):
    user_id = message.from_user.id
    chat_id = message.chat.id
    admin_id = CONFIG["admin_id"]
    if int(user_id) != int(admin_id):
        return
    
    cpu = psutil.cpu_percent(interval=None)
    ram = psutil.virtual_memory()

    text = f"Процессор загружен на: <b>{cpu}%</b>\nПамять загружена на: <b>{ram.percent}%</b>\nБот работает!"
    await telegram_bot.send_message(chat_id,text, parse_mode=ParseMode.HTML)


async def coocking(id, message):
    data = CONFIG[id]
    file = f"static/{data["image"]}"
    caption = data["caption"]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[[types.InlineKeyboardButton(text="🚪ВОЙТИ В ЧАТ",url=f"{data["chat_link"]}")], [types.InlineKeyboardButton(text="📜ПРАВИЛА",url=f"{data["telegraph"]}")]])
    await message_post(chat_id=data["chat_id"], message=message, file_path=file, caption=caption, keyboard=keyboard)


processed_media = set()

@dp.message()
async def handle_telegram_message(message: Message):
    if message.date < START_TIME:
        return
    
    chat_id, id = await data_message(message)

    if message.is_automatic_forward:


        if int(id) in ID_CHANNEL:
            print("Пост от канала!")

            if message.media_group_id:
                key = (id, message.media_group_id)
                if key not in processed_media:
                    processed_media.add(key)
                    await asyncio.sleep(1)
                else:
                    return
            

            await coocking(id, message)

async def main():
    try:
        print("Бот запущен!")
        await dp.start_polling(telegram_bot)
    finally:
        print("Бот выключен")
        await telegram_bot.close()

if __name__ == "__main__":
    asyncio.run(main())