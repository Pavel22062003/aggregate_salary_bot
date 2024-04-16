import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import CommandStart
from app.services.aggregate_manager import AggregateManager
from app.settings import BOT_TOKEN
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


@dp.message(CommandStart())
async def welcome_handler(ms: Message):
    await ms.reply(f'Привет @{ms.chat.username}')


@dp.message()
async def initial_data_handler(ms: Message):
    manager = AggregateManager(data=ms.text)
    result = await manager.process()
    await ms.answer(result)


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
