
#Copyright (c) 2021 SUBIN

from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram import Client, filters
import signal
from utils import USERNAME, FFMPEG_PROCESSES, mp
from config import Config
import os
import sys
import subprocess
import asyncio
from signal import SIGINT
U=USERNAME
CHAT=Config.CHAT
msg=Config.msg
HOME_TEXT = "<b>Helo, [{}](tg://user?id={})\n\nIam a MusicPlayer Bot which plays music in @xreapr.\n\nI can even Stream Youtube Live in Voicechat.\n\nHit /help to know about available commands.</b>"
HELP = """

Use /play <song name> or use /play as a reply to an audio file or youtube link.

You can also use /dplay <song name> to play a song from Deezer.</b>

**Common Commands**:

**/play**  Reply to an audio file or YouTube link to play it or use /play <song name>.
**/dplay** Play music from Deezer, Use /dplay <song name>
**/player**  Show current playing song.
**/help** Show help for commands
**/playlist** Shows the playlist.

**Admin Commands**:
**/skip** [n] ...  Skip current or n where n >= 2
**/join**  Join voice chat.
**/leave**  Leave current voice chat
**/vc**  Check which VC is joined.
**/stop**  Stop playing.
**/radio** Start Radio.
**/stopradio** Stops Radio Stream.
**/replay**  Play from the beginning.
**/clean** Remove unused RAW PCM files.
**/pause** Pause playing.
**/resume** Resume playing.
**/volume** Change volume(0-200).
**/mute**  Mute in VC.
**/unmute**  Unmute in VC.
**/restart** Restarts the Bot.

Support GRoup @xreapr_chat
"""



@Client.on_message(filters.command(['start', f'start@{U}']))
async def start(client, message):
    buttons = [
        [
        InlineKeyboardButton('⚙️ Update Channel', url='https://t.me/xreapr'),
        InlineKeyboardButton('🤖 Support Group', url='https://t.me/xreapr_chat'),
    ],
    [
        InlineKeyboardButton('👨🏼‍💻 Developer', url='https://t.me/reaprx'),
        InlineKeyboardButton('🧩 Source', url='https://github.com/reaprx/tgmusicPlayer'),
    ],
    [
        InlineKeyboardButton('👨🏼‍🦯 Help', callback_data='help'),
        
    ]
    ]
    reply_markup = InlineKeyboardMarkup(buttons)
    m=await message.reply(HOME_TEXT.format(message.from_user.first_name, message.from_user.id), reply_markup=reply_markup)
    await mp.delete(m)
    await mp.delete(message)



@Client.on_message(filters.command(["help", f"help@{U}"]))
async def show_help(client, message):
    buttons = [
        [
             InlineKeyboardButton('⚙️ Update Channel', url='https://t.me/xreapr'),
             InlineKeyboardButton('🤖 Support Group', url='https://t.me/xreapr_chat'),
        ],
        [
            InlineKeyboardButton('👨🏼‍💻 Developer', url='https://t.me/reaprx'),
            InlineKeyboardButton('🧩 Source', url='https://github.com/reaprx/tgmusicPlayer'),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(buttons)
    if msg.get('help') is not None:
        await msg['help'].delete()
    msg['help'] = await message.reply_text(
        HELP,
        reply_markup=reply_markup
        )
    await mp.delete(message)
@Client.on_message(filters.command(["restart", f"restart@{U}"]) & filters.user(Config.ADMINS) & (filters.chat(CHAT) | filters.private))
async def restart(client, message):
    await message.reply_text("🔄 Restarting...")
    await mp.delete(message)
    process = FFMPEG_PROCESSES.get(CHAT)
    if process:
        try:
            process.send_signal(SIGINT)
        except subprocess.TimeoutExpired:
            process.kill()
        except Exception as e:
            print(e)
            pass
        FFMPEG_PROCESSES[CHAT] = ""
    os.execl(sys.executable, sys.executable, *sys.argv)
    
