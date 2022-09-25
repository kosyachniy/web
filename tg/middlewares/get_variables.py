from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware


class VariablesMiddleware(BaseMiddleware):
    async def on_process_message(self, message: types.Message, data: dict):
        print('message')

    async def on_pre_process_callback_query(self, callback: types.CallbackQuery, data: dict):
        print('callback')
