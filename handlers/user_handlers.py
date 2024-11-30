from utils.loader import dp, bot
from utils.db import User

import datetime as dt
from aiogram.types.message import Message
from aiogram.types.dice import DiceEmoji
from aiogram.types.chat_permissions import ChatPermissions
from aiogram.filters.command import Command
from aiogram.methods.delete_message import DeleteMessage
from aiogram import F
from random import randint, choice, random
from emoji import *
from asyncio import sleep

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
        if message.from_user.username == None:
            User.add(message.from_user.id, message.from_user.first_name, message.from_user.first_name)
            return
        User.add(message.from_user.id, message.from_user.username, message.from_user.first_name)
        
    if message.dice.value in winning_nums:
        rand = randint(1, 2)
        User.reset_gamble_lasting_count(message.from_user.id)
        User.add_to_wins_count(message.from_user.id)
        await sleep(2)
        if message.dice.value == 64 and rand == 1:
            await message.answer(choice(syava_videos))
        await message.reply(emojize(":party_popper:Виннер-виннер чикен диннер, счетчик фри спинов сброшен"))
        return
    
    User.add_to_gamble_lasting_count(message.from_user.id)
    User.add_to_gamble_total_count(message.from_user.id)
    
    if User.get_gamble_lasting_count(message.from_user.id) == 7:
        User.reset_gamble_lasting_count(message.from_user.id)
        await message.chat.restrict(user_id=message.from_user.id, permissions=mute_perms, until_date=dt.timedelta(minutes=1))
        await sleep(2)
        await message.reply(emojize(":no_entry:Истрачены все спины, пользователь замучен на 1 минуту"))
        return
        
    msg_count = 7 - User.get_gamble_lasting_count(message.from_user.id)
    
    await sleep(2)
    msg = await message.answer(emojize(f":slightly_frowning_face:{message.from_user.first_name} анлаки\nОсталось спинов: {msg_count}"))
    await message.delete()
    await sleep(2)
    await bot(DeleteMessage(chat_id=message.chat.id, message_id=msg.message_id))
    
@dp.message(Command("leaderboard"))
async def leaderboard_handler(message: Message):
    board = ""

    users = User.get_all()

    users.sort(key=sort_by_total_score, reverse=True)
    
    top10 = users[:10]

    for user in top10:
        board += emojize(f"{user[1]} ({user[0]}):\n\t\t\t:input_numbers:Всего: {user[2]}\n\t\t\t:party_popper:Выиграно: {user[3]}\n\n")
        
    await message.answer(emojize(":TOP_arrow:ТОП-10 гэмблеров:\n\n" + board))
        
def sort_by_total_score(user):
    return user[2]