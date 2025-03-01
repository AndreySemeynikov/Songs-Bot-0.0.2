from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
import logging

logger = logging.getLogger(__name__)

start_router = Router()

@start_router.message(CommandStart())
async def cmd_start(message: Message):
    """
        Handles the /start command and sends a welcome message.
        """
    welcome_text = "Welcome! Please send me a search query to find files."
    logger.info(f"User {message.from_user.id} started the bot.")
    await message.answer(welcome_text)

