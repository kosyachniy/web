"""
Get variable middleware
"""

from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware


class VariablesMiddleware(BaseMiddleware):
    """ Variables middleware """

    async def on_process_message(self, message: types.Message, data: dict):
        """ Message """
        print('message')

    async def on_pre_process_callback_query(
        self, callback: types.CallbackQuery, data: dict,
    ):
        """ Callback """
        print('callback')
