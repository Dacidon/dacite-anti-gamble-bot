from os import getenv

from aiogram import Bot, Dispatcher, enums
from aiogram.client.default import DefaultBotProperties

TOKEN=getenv("TG_API_TOKEN")

dp = Dispatcher()
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=enums.ParseMode.HTML))