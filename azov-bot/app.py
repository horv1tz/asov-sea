import asyncio
import os

from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.strategy import FSMStrategy
from aiogram.types import Message

from dotenv import find_dotenv, load_dotenv

from kbds.reply import get_keyboard

load_dotenv(find_dotenv())

from handlers.troubles import user_private_router

ALLOWED_UPDATES = ['message, edited_message']

bot = Bot(token=os.getenv('TOKEN'), parse_mode=ParseMode.HTML)
bot.my_admins_list = []

storage = MemoryStorage()
# При создании Dispatcher передайте storage:
dp = Dispatcher(storage=storage)

dp.include_router(user_private_router)

@dp.message(CommandStart())
async def command_start_handler(message: Message):
    await message.answer(
        """
        Здравствуйте!\n Я помогу очистить Богудонию, рыбацкий район у моря от экологических проблем.\n Вы можете отправить мне данные о проблеме и тогда свободные активисты смогут приступить к её решению!
        """,
        reply_markup=get_keyboard(
            "отправить данные о проблеме",
            placeholder="Выберите действие",
            sizes=(1,),
        )
    )

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    # await bot.delete_my_commands(scope=types.BotCommandScopeAllPrivateChats())
    await dp.start_polling(bot, allowed_updates=ALLOWED_UPDATES)

asyncio.run(main())
