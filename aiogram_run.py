import logging
import asyncio
from create_bot import bot, dp
from handlers.start import start_router
from handlers.search import search_router


# from work_time.time_func import send_time_msg

logger = logging.getLogger(__name__)


async def main():
    # scheduler.add_job(send_time_msg, 'interval', seconds=10)
    # scheduler.start()
    dp.include_router(start_router)
    dp.include_router(search_router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    # todo call function from file_manager to create dictionary
    logger.info("Starting bot polling...")
    asyncio.run(main())
