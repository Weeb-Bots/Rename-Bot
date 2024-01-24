import math
import anitopy
import os
import re
import time

from pyrogram.errors import FloodWait
from pyrogram.types import Message
from asyncio import sleep as slp
from pyrogram.types import Message
from config import Config


captom = {}


def get_readable_time(seconds):
    intervals = [('day', 86400), ('hour', 3600), ('minute', 60), ('second', 1)]
    time_parts = []

    for unit, value in intervals:
        if seconds >= value:
            count = seconds // value
            seconds %= value
            time_parts.append(f"{count} {unit}{'s' if count != 1 else ''}")

    return ', '.join(time_parts) or '0 seconds'


def hbs(size):
    units = ['B', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB']
    i = 0
    while size >= 1024 and i < len(units) - 1:
        size /= 1024.0
        i += 1

    return f"{size:.2f} {units[i]}"



async def progress_for_pyrogram(
  current,
  total,
  ud_type,
  msg: Message,
  start
):
  diff = time.time() - start
  if round(diff % 10.00) == 0 or current == total:
    percentage = current * 100 / total
    speed = current / diff
    elapsed_time = round(diff) * 1000
    time_to_completion = round((total - current) / speed) * 1000
    estimated_total_time = elapsed_time + time_to_completion

    elapsed_time = get_readable_time(elapsed_time)
    estimated_total_time = get_readable_time(estimated_total_time)

    progress = "[{0}{1}] \n**Percentage:** {2}%\n".format(
      ''.join(["▣" for i in range(math.floor(percentage / 10))]),
      ''.join(["□" for i in range(10 - math.floor(percentage / 10))]),
      round(percentage, 2))

    tmp = progress + "**• Completed :** {0}\n➖➖➖➖➖➖➖➖➖➖➖➖➖\n**• Size :** {1}\n➖➖➖➖➖➖➖➖➖➖➖➖➖\n**• Speed :** {2}/s\n➖➖➖➖➖➖➖➖➖➖➖➖➖\n**• ETA :** {3}\n".format(
      hbs(current),
      hbs(total),
      hbs(speed),
      estimated_total_time if estimated_total_time != '' else "0 s"
    )
    try:
      await msg.edit_text(f"{ud_type}\n{tmp}")
    except:
      pass



async def upload_file(file: str, msg: Message, edit: Message):
  """
  Uploading Files
  """
  if msg.from_user.id in captom:
     cap = captom[msg.from_user.id]
  else:
     cap = f"**〶** `{file.split('/')[-1]}`\n\n{Config.DF_CAP}"
  thum = f"./downloads/thumb/{msg.from_user.id}.jpeg" if os.path.exists(f"./downloads/thumb/{msg.from_user.id}.jpeg") else "./downloads/thumb/df.jpeg"
  await slp(1)
  try:
    c_time= time.time()
    await msg.reply_document(file,
                   quote=True,
                   thumb=thum,
                   caption=cap,
                   force_document=True,
                   progress=progress_for_pyrogram,
                   progress_args=("𝚄𝙿𝙻𝙾𝙰𝙳𝙸𝙽𝙶 𝚃𝙾 𝚃𝙴𝙻𝙴𝙶𝚁𝙰𝙼",edit,c_time)
          )
  except FloodWait as e:
    await slp(e.value)
    await upload_file(file, msg, edit)


async def progress(current, total, msg, name, wh):
  """
  Pyrogram Progress
  """
  percent = round(current*100/total, 2)
  ct = hbs(current)
  tot = hbs(total)
  text = f"**{name}**\n\n**{wh}:** {ct}\n\n**♻️ Progress:** `{percent}%`\n\n**📀 Total:** `{tot}`"
  try:
     await msg.edit_text(text)
  except:
     pass

async def process_file(m: Message, new_name: str):
  msg = await m.reply_text("`Now 📥Downloading The File`", quote=True)
  dl = await m.download(file_name=new_name, progress=progress, progress_args=(msg, "𝙳𝙾𝚆𝙽𝙻𝙾𝙰𝙳𝙸𝙽𝙶 𝚃𝙾 𝚂𝙴𝚁𝚅𝙴𝚁", "📥 Downloaded"))
  await msg.edit_text(f"**Downloading Completed** \n\n**Location:** `{dl}`")
  await slp(2)
  await msg.edit_text("```Now 📝Renaming The File\n```")
  await slp(2)
  await msg.edit_text("```Now 📤Uploading The File\n```")
  await upload_file(new_name, msg=m, edit=msg)
  await msg.delete()
  try:
     os.remove(dl)
  except:
     pass
  await slp(2)