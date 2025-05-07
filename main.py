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


startTime = time.time()
prefix = ["/", ";", "?", "!", ".", ":", "-"]

uvloop.install()
app = Client("Renamer",
        api_id=Config.API_ID,
        api_hash=Config.API_HASH,
        bot_token=Config.BOT_TOKEN,
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
    txt = "Nothin Much To Help.\n**Just Send Your Video or Doc To Rename\nExample:**\n```Format\n/rename Xyz.mp4\n```\n\nCan Also Convert Vid -> Doc and Vice Versa Just Use ```/convert```"
    await msg.reply_text(txt, quote=True)



@app.on_message(filters.photo & filters.private)
async def photo_save(_, m: Message):
  thumb = "downloads/thumb/" + str(m.from_user.id) + ".jpeg"
  if os.path.exists(thumb):
      os.remove(thumb)
  await m.download(file_name=thumb)
  await m.reply_text("✅ʏᴏᴜʀ ᴘʜᴏᴛᴏ ʜᴀꜱ ʙᴇᴇɴ ꜱᴀᴠᴇᴅ ᴀꜱ ʏᴏᴜʀ ᴛʜᴜᴍʙɴᴀɪʟ.", quote=True)


@app.on_message(filters.incoming & filters.private & filters.reply & filters.audio & filters.document & filters.document)
async def reanamer(_, m: Message):
    n_msg = await m.ask(text="Reply With **New Filename With Extension:**", timeout=60, filters=filters.text, reply_markup=ForceReply(selective=True, placeholder="New Filename+Extension:"))
    filenaam = f"./downloads/{n_msg.text}"
    await n_msg.delete()
    msg = await m.reply_text("`Now 📥Downloading The File`", quote=True)
    c_time= time.time()
    try:
        dl_loc = await m.download(
              block=False,
              file_name=filenaam, 
              progress=progress_for_pyrogram, 
              progress_args=("Dᴏᴡɴʟᴏᴀᴅɪɴɢ ᴛᴏ sᴇʀᴠᴇʀ", msg, c_time))
    except:
        try:
            os.remove(filenaam)
        except:
            pass
        return await m.reply("Download Failed")
    await msg.edit_text(f"**Download Completed📥**")
    await slp(2)
    await msg.edit_text("**Now 📝Renaming The File.**")
    await slp(2)
    await msg.edit_text("**Now Uploading The File.📤**")
    await upload_file(new_name, msg=m, edit=msg)
    await msg.delete()
    try:
        os.remove(dl)
    except:
        pass



@app.on_message(filters.incoming & filters.private & filters.command(commands="set", prefixes=prefix))
async def setting(_, m: Message):
    text = m.text
    if not " " in text:
        return await m.reply_text("**Sending Format:-**\n```Format\n/set Hello \\n\\n**⌬ Uploaded By @Anime_Pile**\n\n```", quote=True)
    text = text.split(" ", 1)[-1]
    captom[m.from_user.id] = text



@app.on_message(filters.incoming & filters.private & filters.command(commands="clear", prefixes=prefix))
async def clear_cmd(_, m: Message):
    if captom.pop(m.from_user.id, False):
        await m.reply_text("**Cleared Successfully✅**", quote=True)
    await m.reply_text("**You Don't Have Anything**", quote=True)


@app.on_message(filters.incoming & filters.private & filters.command(commands=["restart","re"], prefixes=prefix))
async def restart_cmd(_, m: Message):
  await m.reply_text("Restarting Bot")
  quit(1)


if __name__ == "__main__":
  app.run()
