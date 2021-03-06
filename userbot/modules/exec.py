"""Execute GNU/Linux commands inside Telegram
Syntax: .exec Code"""

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import time
import asyncio
import io
import subprocess
from telethon.errors import MessageEmptyError, MessageTooLongError, MessageNotModifiedError
from userbot import bot, CMD_HELP
from userbot.events import register


@register(outgoing=True, pattern="^.exec(?: |$)(.*)")
async def _(event):
    if event.fwd_from:
        return
    DELAY_BETWEEN_EDITS = 0.3
    PROCESS_RUN_TIME = 100
    cmd = event.pattern_match.group(1)
    reply_to_id = event.message.id
    if event.reply_to_msg_id:
        reply_to_id = event.reply_to_msg_id
    c_time = time.time() + PROCESS_RUN_TIME
    process = await asyncio.create_subprocess_shell(
        cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    OUTPUT = f"**QUERY:**\n__Command:__\n`{cmd}` \n__PID:__\n`{process.pid}`\n\n**Output:**\n"
    stdout, stderr = await process.communicate()
    if len(stdout) > Config.MAX_MESSAGE_SIZE_LIMIT:
        with io.BytesIO(stdout) as out_file:
            out_file.name = "exec.text"
            await bot.send_file(
                event.chat_id,
                out_file,
                force_document=True,
                allow_cache=False,
                caption=OUTPUT,
                reply_to=reply_to_id
            )
            await event.delete()
        return
    if stderr.decode():
        await event.edit(f"{OUTPUT}`{stderr.decode()}`")
        return
    await event.edit(f"{OUTPUT}`{stdout.decode()}`")
    
    CMD_HELP.update({
    "exec": 
    ".exec <code> \
        \nUsage: Performing Linux Commands in Telegram\n"
    })
