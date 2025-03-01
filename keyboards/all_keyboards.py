from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram_widgets.pagination import KeyboardPaginator


# todo move to inline keyboards
def create_file_keyboard_paginator(matching_files: list, current_page: int, query: str):
    """
    Creates an inline keyboard paginator for the given list of matching files.

    :param matching_files: List of file names.
    :param current_page: Current page number.
    :param query: The search query (to be passed in navigation callback data).
    :return: InlineKeyboardMarkup generated by KeyboardPaginator.
    """
    # Create buttons for each file with callback data formatted as "file_<file_name>"
    buttons = [InlineKeyboardButton(text=file_name, callback_data=f"file_{file_name}")
               for file_name in matching_files]

    # Prepare navigation buttons:
    # If current page is 1, disable "Previous" by setting callback data to "ignore"
    prev_callback = f"page_{current_page - 1}_{query}" if current_page > 1 else "ignore"
    next_callback = f"page_{current_page + 1}_{query}"
    additional_buttons = [
        [
            InlineKeyboardButton(text="Previous", callback_data=prev_callback),
            InlineKeyboardButton(text="Next", callback_data=next_callback)
        ]
    ]

    paginator = KeyboardPaginator(
        data=buttons,
        additional_buttons=additional_buttons,
        per_page=10,  # 10 buttons per page
        per_row=2  # 2 buttons per row
    )
    # Set the current page if needed by the paginator (depends on library implementation)
    paginator.current_page = current_page

    return paginator.as_markup()
