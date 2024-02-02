import os
import time
import wget
import uvloop
import asyncio

from utils import *
from config import Config

from asyncio import sleep as slp
from pyrogram import Client, filters
from pyrogram.types import Message


uvloop.install()
startTime = time.time()

prefix = ["/", ";", "?", "!", ".", ":", "-"]
app = Client("Renamer",
        api_id=Config.API_ID,
        api_hash=Config.API_HASH,
        bot_token=Config.BOT_TOKEN,
        in_memory=True,
        workers=50   #Don't Touch If Dont Know
     )
print("<--Pyrogram Client Built-->")


if not os.path.isdir("./downloads/"):
   os.mkdir("./downloads/")
   os.mkdir("./downloads/thumb/")
wget.download(Config.DF_THUMB, "./downloads/thumb/df.jpeg")


@app.on_message(filters.incoming & filters.command(commands="start", prefixes=prefix))
async def start_help(_, m: Message):
  st_img = "https://te.legra.ph//file/099e9d2ee0565cd3c2418.jpg"
  ct = time.time()
  ctime = get_readable_time(ct - startTime)
  text = "Hello __{}__,\n**This Is One Of The Fastest Telegram Renamer Bots That Are Currently Available.**\n\n**Bot Uptime:** __{}__".format(m.from_user.mention(style="md"), ctime)
  await m.reply_photo(st_img, caption=text, quote=False)



@app.on_message(filters.incoming & filters.private & filters.command(commands="help", prefixes=prefix))
async def help_(_: Client, msg: Message):
    txt = "Nothin Much To Help.\n**Just Send Your Video or Doc To Rename\nExample:**\n```/rename Xyz.mp4\n```\n\nCan Also Convert Vid -> Doc and Vice Versa Just Use ```/convert```"
    await msg.reply_text(txt, quote=True)



@app.on_message(filters.photo & filters.private)
async def photo_save(_, m: Message):
  thumb = "downloads/thumb/" + str(m.from_user.id) + ".jpeg"
  if os.path.exists(thumb):
      os.remove(thumb)
  await m.download(file_name=thumb)
  await m.reply_text("✅ʏᴏᴜʀ ᴘʜᴏᴛᴏ ʜᴀꜱ ʙᴇᴇɴ ꜱᴀᴠᴇᴅ ᴀꜱ ʏᴏᴜʀ ᴛʜᴜᴍʙɴᴀɪʟ.", quote=True)


@app.on_message(filters.incoming & filters.private & filters.reply & filters.command(commands="rename", prefixes=prefix))
async def reanamer(_, msg: Message):
    if len(msg.command) < 2:
        return await msg.reply("Provide a Filename to Rename")
    new_name = " ".join(msg.command[1:])
    reply_to = msg.reply_to_message
    if not str(reply_to.media).split('.')[-1] in "VIDEOAUDIODOCUMENT":
        return await msg.reply("Provide a Proper File To Rename", quote=True)
    # type = str(reply_to.media).split('.')[-1].lower() # Later Verion 
    _dl = os.path.join( "./downloads", new_name)

    asyncio.create_task(process_file(reply_to, _dl))
    #await process_file(reply_to, _dl)
    



@app.on_message(filters.incoming & filters.private & filters.command(commands="set", prefixes=prefix))
async def setting(_, m: Message):
    text = m.text
    if not " " in text:
        return await m.reply_text("**Sending Format:-**\n```/set Hello \/n\/n**⌬ Uploaded By @Anime_Pile**\n\n```", quote=True)
    text = text.split(" ", 1)[-1]
    captom[m.from_user.id] = text



@app.on_message(filters.incoming & filters.private & filters.command(commands="clear", prefixes=prefix))
async def clear_cmd(_, m: Message):
    if m.from_user.id in captom:
        captom.pop('key2', None)
        await m.reply_text("**Cleared Successfully✅**", quote=True)
    await m.reply_text("**You Don't Have Anything**", quote=True)


@app.on_message(filters.incoming & filters.private & filters.command(commands=["restart","re"], prefixes=prefix))
async def restart_cmd(_, m: Message):
  await m.reply_text("Restarting Bot")
  quit(1)

print("<-- Bot Started Working -->")
app.run()
