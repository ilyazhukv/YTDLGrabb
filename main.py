import asyncio
from os import getenv

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

from handlers.routes import router

load_dotenv()
TOKEN = getenv("BOT_TOKEN")

dp = Dispatcher()
dp.include_router(router)

async def main():
    if TOKEN is None:
        print("Token not found")
        return

    bot = Bot(token=TOKEN)

    print("Start..")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
