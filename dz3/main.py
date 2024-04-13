import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.utils.markdown import hbold
from aiogram.filters.command import Command
from aiogram.client.session.aiohttp import AiohttpSession

TOKEN = "6397148691:AAG0QzG6dpDhGpoqETpkiwpQs2r4cWANL8w"
PROXY = "http://proxy.server:3128"

dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Hello, {hbold(message.from_user.first_name)}!")


async def main() -> None:
    session = AiohttpSession(proxy=PROXY)
    bot = Bot(TOKEN, session=session, parse_mode=ParseMode.HTML)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
