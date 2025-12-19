import asyncio
from aiogram import Bot,  Dispatcher
from aiogram.types import BotCommand
# from config import *
from JobFlow.jobflow.telegram_bot.handlers import *
from JobFlow.config import *
# from middlewares import LoggingMiddleware


# Создаем экземпляры бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# dp.message.middleware(LoggingMiddleware())
dp.include_router(router)
dp.startup.register(start_background_tasks)



async def main():
    
    # Запускаем фоновую задачу для обновлений
    # asyncio.create_task(hourly_task())
    
    # Запускаем бота
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
   