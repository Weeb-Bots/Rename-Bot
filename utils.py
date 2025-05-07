import math
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

    return ', '.join(time_parts) or '0s'


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
  if round(diff % 04.00) == 0 or current == total:
    percentage = current * 100 / total
    speed = current / diff
    estimated_total_time = get_readable_time((total - current) / speed)

    sr = math.floor(percentage / 10)
    progress = "[{0}{1}] \n**Percentage:** {2}%\n".format(
      ''.join(["▣" for i in range(sr)]),
      ''.join(["□" for i in range(10 - sr)]),
      round(percentage, 2))

    tmp = progress + "**• Completed :** {0}\n\n**• Size :** {1}\n\n**• Speed :** {2}/s\n\n**• ETA :** {3}\n".format(
      hbs(current),
      hbs(total),
      hbs(speed),
      estimated_total_time
    )
    try:
      await msg.edit_text(f"{ud_type}\n{tmp}")
    except:
      pass


async def upload_file(file: str, msg: Message, edit: Message):
  """
  Uploading Files
  """
  name = file.split('/')[-1]
  if msg.from_user.id in captom:
     cap = captom[msg.from_user.id].format(name = name)
  else:
     cap = f"**〶** `{name}`\n\n{Config.DF_CAP}"
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
    await slp(e.value + 2)
    await upload_file(file, msg, edit)
