from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
import logging

from aiogram.utils.chat_action import ChatActionSender

from create_bot import bot, admins
from keyboards.all_keyboards import main_kb, home_page_kb

logger = logging.getLogger(__name__)

start_router = Router()


@start_router.message(CommandStart())
async def cmd_start(message: Message):
    """
        Handles the /start command and sends a welcome message.
        """
    welcome_text = "Welcome! Please send me a search query to find files."
    logger.info(f"User {message.from_user.id} started the bot.")

    current_commands = await bot.get_my_commands()
    logger.info(current_commands)
    await message.answer(text=welcome_text, reply_markup=main_kb(message.from_user.id))


@start_router.message((F.text.endswith('Админ панель')) & (F.from_user.id.in_(admins)))
async def get_greeting(message: Message):
    async with ChatActionSender.typing(bot=bot, chat_id=message.from_user.id):
        admin_text = f'Привет админ с id: {message.from_user.id} и username: {message.from_user.username}'
    await message.answer(admin_text, reply_markup=home_page_kb(message.from_user.id))


@start_router.message(F.text.contains('Назад'))
async def cmd_start(message: Message):
    await message.answer(f'{message.from_user.first_name}, Нажата кнопка назад.',
                         reply_markup=main_kb(message.from_user.id))

@start_router.message(Command('profile'))
@start_router.message(F.text.contains('Мой профиль'))
async def get_profile(message: Message):
    async with ChatActionSender.typing(bot=bot, chat_id=message.from_user.id):
        text = (f'👉 Ваш телеграм ID: <code><b>{message.from_user.id}</b></code>\n'
                f'Ваш username: <code><b>{message.from_user.username}</b></code>\n'
                f'Ваше имя: <code><b>{message.from_user.first_name}</b></code>\n'
                f'Ваша фамилия: <code><b>{message.from_user.last_name}</b></code>\n'
                )
    await message.answer(text, reply_markup=home_page_kb(message.from_user.id))


@start_router.message(Command('hello'))
async def hello(message: Message):
    await message.answer(f'{message.from_user.first_name}, Выполнена команда /hello.',
                         reply_markup=main_kb(message.from_user.id))