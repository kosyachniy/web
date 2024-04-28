from aiogram import Bot

from libdev.cfg import cfg


bot = Bot(token=cfg("tg.token"))


__all__ = ("bot",)
