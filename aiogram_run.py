import logging
import asyncio

from aiogram.types import BotCommand, BotCommandScopeDefault

from create_bot import bot, dp, admins
from handlers.start import start_router
from handlers.search import search_router


# from work_time.time_func import send_time_msg

logger = logging.getLogger(__name__)

async def set_commands():
    commands = [BotCommand(command='hello', description='Поздороваться'),
                BotCommand(command='start', description="Старт"),
                BotCommand(command='profile', description='Мой профиль'),
                ]
    await bot.set_my_commands(commands, BotCommandScopeDefault())

async def stop_bot():
    try:
        for admin_id in admins:
            await bot.send_message(admin_id, 'Бот остановлен. За что?😔')
    except:
        pass

async def start_bot():
    await set_commands()
    try:
        for admin_id in admins:
            await bot.send_message(admin_id, f'Я запущен🥳')
    except:
        pass


async def main():
    # scheduler.add_job(send_time_msg, 'interval', seconds=10)
    # scheduler.start()
    dp.include_router(start_router)
    dp.include_router(search_router)

    # регистрация функций при старте и завершении работы бота
    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)

    current_commands = await bot.get_my_commands()
    logger.info(current_commands)

    # запуск бота в режиме long polling при запуске бот очищает все обновления, которые были за его моменты бездействия
    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    finally:
        await bot.session.close()


if __name__ == "__main__":
    # todo call function from file_manager to create dictionary
    logger.info("Starting bot polling...")
    asyncio.run(main())
