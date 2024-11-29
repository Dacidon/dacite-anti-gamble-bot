from utils.loader import dp
from utils.db import User

import datetime as dt
from aiogram.types.message import Message
from aiogram.types.dice import DiceEmoji
from aiogram.types.chat_permissions import ChatPermissions
from aiogram.filters.command import Command
from aiogram import F
from random import randint, choice

winning_nums = (1, 22, 43, 64)

mute_perms = ChatPermissions(
    can_send_audios=False,
    can_send_documents=False,
    can_send_messages=False,
    can_send_other_messages=False,
    can_send_photos=False,
    can_send_polls=False,
    can_send_video_notes=False,
    can_send_videos=False,
    can_send_voice_notes=False
)

syava_videos = (
    "https://www.youtube.com/watch?v=MiXRkmamHu0",
    "https://www.youtube.com/watch?v=OCY7RVlzONk",
    "https://www.youtube.com/watch?v=QQ0Nu3P0_xw",
    "https://www.youtube.com/watch?v=2_TiiBIrwu4",
    "https://www.youtube.com/watch?v=AXlZTIG3qMM",
    "https://www.youtube.com/watch?v=KrmQUtKS-pY"
)

@dp.message(F.dice.emoji == DiceEmoji.SLOT_MACHINE)
async def slot_handler(message: Message):
    if not User.find(message.from_user.id):
        User.add(message.from_user.id)
        
    if message.dice.value in winning_nums:
        User.reset_gamble_daily_count(message.from_user.id)
        User.add_to_wins_count(message.from_user.id)
        if message.dice.value == 64 and randint(1, 2):
            await message.answer(choice(syava_videos))
        await message.reply("Победное значение, счетчик ежедневных фри спинов сброшен")
        return
    
    User.add_to_gamble_daily_count(message.from_user.id)
    User.add_to_gamble_total_count(message.from_user.id)
    
    if User.get_gamble_daily_count(message.from_user.id) == 7:
        User.reset_gamble_daily_count(message.from_user.id)
        await message.chat.restrict(user_id=message.from_user.id, permissions=mute_perms, until_date=dt.timedelta(minutes=5))
        await message.reply("Превышено максимальное количество фри спинов за день, пользователь замучен на 5 минут")
        return
        
    await message.answer(f"{message.from_user.first_name}(@{message.from_user.username}) анлаки. Осталось фри спинов: {7 - User.get_gamble_daily_count(message.from_user.id)}")
    await message.delete()
    
