import logging
from aiogram.types import Message, InlineKeyboardButton, CallbackQuery

from aiogram import Router
from aiogram_widgets.pagination import KeyboardPaginator

from create_bot import dp, bot

from decouple import config

logger = logging.getLogger(__name__)
search_router = Router()


@search_router.message()
async def search_message_handler(message: Message):
    """
    Handles text messages by performing a file search and sending an inline keyboard paginator.
    """
    query = message.text.strip()
    if not query:
        await message.answer("Please provide a non-empty query.")
        return

    doc_store = dp["doc_store"]
    matching_docs = doc_store.search_by_content(query)
    if not matching_docs:
        await message.answer("No matching files found.")
        return

    buttons = [
        InlineKeyboardButton(text=doc.filename, callback_data=f"file_{doc.id}")
        for doc in matching_docs
    ]

    paginator = KeyboardPaginator(
        data=buttons,
        router=search_router,
        per_page=config('DOCUMENTS_PER_PAGE'),
        per_row=int(config('DOCUMENTS_PER_ROW')),
    )

    logging.info(f"User {message.from_user.id} searched for '{query}' and found {len(matching_docs)} files.")
    await message.answer("Matching files:", reply_markup=paginator.as_markup())


@search_router.callback_query(lambda c: c.data.startswith("file_"))
async def file_callback_handler(callback_query: CallbackQuery):
    """
    Handles callback queries for file selections.
    Retrieves the document by its short id from the DocumentStore
    and sends its content.
    """

    doc_id = callback_query.data.split("_")[1]

    doc_store = dp.get("doc_store")
    if doc_store is None:
        await callback_query.answer("Document store not found.", show_alert=True)
        return

    document = doc_store.get_by_id(doc_id)
    if document is None:
        await callback_query.answer("Document not found.", show_alert=True)
        return

    await callback_query.message.answer(
        f"Content of {document.filename}:\n\n{document.content}"
    )

    message_id = callback_query.message.message_id
    chat_id = callback_query.message.chat.id

    await bot.delete_message(chat_id, message_id)
