import asyncio
import random
from ArcaneUserbot.helpers.command import commandpro
from ArcaneUserbot.helpers.decorators import errors, sudo_users_only
from pyrogram import Client
from pyrogram.types import Message
from pytgcalls import StreamType
from pytgcalls.types.input_stream import AudioPiped, AudioVideoPiped
from pytgcalls.types.input_stream.quality import (
    HighQualityAudio,
    HighQualityVideo,
    LowQualityVideo,
    MediumQualityVideo,
)
from youtubesearchpython import VideosSearch

from config import bot, call_py
from ArcaneUserbot.helpers.queues import QUEUE, add_to_queue, get_queue

# music player
def ytsearch(query):
    try:
        search = VideosSearch(query, limit=1)
        for r in search.result()["result"]:
            ytid = r["id"]
            if len(r["title"]) > 34:
                songname = r["title"][:35] + "..."
            else:
                songname = r["title"]
            url = f"https://www.youtube.com/watch?v={ytid}"
        return [songname, url]
    except Exception as e:
        print(e)
        return 0


async def ytdl(link):
    proc = await asyncio.create_subprocess_exec(
        "yt-dlp",
        "-g",
        "-f",
        # CHANGE THIS BASED ON WHAT YOU WANT
        "bestaudio",
        f"{link}",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await proc.communicate()
    if stdout:
        return 1, stdout.decode().split("\n")[0]
    else:
        return 0, stderr.decode()


# video player
def ytsearch(query):
    try:
        search = VideosSearch(query, limit=1)
        for r in search.result()["result"]:
            ytid = r["id"]
            if len(r["title"]) > 34:
                songname = r["title"][:35] + "..."
            else:
                songname = r["title"]
            url = f"https://www.youtube.com/watch?v={ytid}"
        return [songname, url]
    except Exception as e:
        print(e)
        return 0


async def ytdl(link):
    proc = await asyncio.create_subprocess_exec(
        "yt-dlp",
        "-g",
        "-f",
        # CHANGE THIS BASED ON WHAT YOU WANT
        "best[height<=?720][width<=?1280]",
        f"{link}",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await proc.communicate()
    if stdout:
        return 1, stdout.decode().split("\n")[0]
    else:
        return 0, stderr.decode()


@Client.on_message(commandpro(["!play", ".play", "/play", "P", "Play"]))
@errors
@sudo_users_only
async def play(client, m: Message):
    replied = m.reply_to_message
    chat_id = m.chat.id
    m.chat.title
    if replied:
        if replied.audio or replied.voice:
            await m.delete()
            huehue = await replied.reply("**🔄 𝑷𝒓𝒐𝒄𝒆𝒔𝒔𝒊𝒏𝒈...**")
            dl = await replied.download()
            link = replied.link
            if replied.audio:
                if replied.audio.title:
                    songname = replied.audio.title[:35] + "..."
                else:
                    songname = replied.audio.file_name[:35] + "..."
            elif replied.voice:
                songname = "Voice Note"
            if chat_id in QUEUE:
                pos = add_to_queue(chat_id, songname, dl, link, "Audio", 0)
                await huehue.delete()
                # await m.reply_to_message.delete()
                await m.reply_text(f"""
**⃣ 𝑺𝒐𝒏𝒈 𝒊𝒏 𝒒𝒖𝒆𝒖𝒆 𝒕𝒐 {pos}
🎵 𝑶𝒏 𝒓𝒆𝒒𝒖𝒆𝒔𝒕 {m.from_user.mention}**
""",
                )
            else:
                await call_py.join_group_call(
                    chat_id,
                    AudioPiped(
                        dl,
                    ),
                    stream_type=StreamType().pulse_stream,
                )
                add_to_queue(chat_id, songname, dl, link, "Audio", 0)
                await huehue.delete()
                # await m.reply_to_message.delete()
                await m.reply_text(f"""
**▶️ 𝑺𝒕𝒂𝒓𝒕𝒆𝒅 𝒑𝒍𝒂𝒚𝒊𝒏𝒈 𝒔𝒐𝒏𝒈
🎵 𝑶𝒏 𝒓𝒆𝒒𝒖𝒆𝒔𝒕 {m.from_user.mention}**
""",
                )

    else:
        if len(m.command) < 2:
            await m.reply("💫 𝑹𝒆𝒑𝒍𝒚 𝒕𝒐 𝒂𝒏 𝒂𝒖𝒅𝒊𝒐 𝒇𝒊𝒍𝒆 𝒐𝒓 𝒑𝒓𝒐𝒗𝒊𝒅𝒆 𝒔𝒐𝒎𝒆𝒕𝒉𝒊𝒏𝒈 𝒇𝒐𝒓 𝒔𝒆𝒂𝒓𝒄𝒉")
        else:
            await m.delete()
            huehue = await m.reply("🔎 𝑺𝒆𝒂𝒓𝒄𝒉𝒊𝒏𝒈...")
            query = m.text.split(None, 1)[1]
            search = ytsearch(query)
            if search == 0:
                await huehue.edit("`❌ 𝑭𝒐𝒖𝒏𝒅 𝒏𝒐𝒕𝒉𝒊𝒏𝒈 `")
            else:
                songname = search[0]
                url = search[1]
                hm, ytlink = await ytdl(url)
                if hm == 0:
                    await huehue.edit(f"**𝒀𝑻𝑫𝑳 𝑬𝒓𝒓𝒐𝒓... ⚠️** \n\n`{ytlink}`")
                else:
                    if chat_id in QUEUE:
                        pos = add_to_queue(chat_id, songname, ytlink, url, "Audio", 0)
                        await huehue.delete()
                        # await m.reply_to_message.delete()
                        m.reply_text(f"""
**⃣ 𝑨𝒅𝒅𝒆𝒅 𝒊𝒏 𝒒𝒖𝒆𝒖𝒆 𝒂𝒕 {pos}
🎵 𝑶𝒏 𝒓𝒆𝒒𝒖𝒆𝒔𝒕 {m.from_user.mention}**
""",
                        )
                    else:
                        try:
                            await call_py.join_group_call(
                                chat_id,
                                AudioPiped(
                                    ytlink,
                                ),
                                stream_type=StreamType().pulse_stream,
                            )
                            add_to_queue(chat_id, songname, ytlink, url, "Audio", 0)
                            await huehue.delete()
                            # await m.reply_to_message.delete()
                            await m.reply_text(f"""
**▶️ 𝑺𝒕𝒂𝒓𝒕𝒆𝒅 𝒑𝒍𝒂𝒚𝒊𝒏𝒈 𝒔𝒐𝒏𝒈
🎵 𝑶𝒏 𝒓𝒆𝒒𝒖𝒆𝒔𝒕 {m.from_user.mention}**
""",
                            )
                        except Exception as ep:
                            await huehue.edit(f"`{ep}`")


@Client.on_message(commandpro([".vplay", "V", "!vplay", "/vplay", "Vplay"]))
@errors
@sudo_users_only
async def vplay(client, m: Message):
    replied = m.reply_to_message
    chat_id = m.chat.id
    m.chat.title
    if replied:
        if replied.video or replied.document:
            await m.delete()
            huehue = await replied.reply("**🔄 𝑷𝒓𝒐𝒄𝒆𝒔𝒔𝒊𝒏𝒈...**")
            dl = await replied.download()
            link = replied.link
            if len(m.command) < 2:
                Q = 720
            else:
                pq = m.text.split(None, 1)[1]
                if pq == "720" or "480" or "360":
                    Q = int(pq)
                else:
                    Q = 720
                    await huehue.edit(
                        "`𝑶𝒏𝒍𝒚 720𝒑, 480𝒑, 360𝒑 𝒂𝒍𝒍𝒐𝒘𝒆𝒅` \n`𝑵𝒐𝒘 𝒔𝒕𝒓𝒆𝒂𝒎𝒊𝒏𝒈 𝒊𝒏 720𝒑`"
                    )

            if replied.video:
                songname = replied.video.file_name[:35] + "..."
            elif replied.document:
                songname = replied.document.file_name[:35] + "..."

            if chat_id in QUEUE:
                pos = add_to_queue(chat_id, songname, dl, link, "Video", Q)
                await huehue.delete()
                # await m.reply_to_message.delete()
                await m.reply_text(f"""
**⃣ 𝑽𝒊𝒅𝒆𝒐 𝒊𝒏 𝒒𝒖𝒆𝒖𝒆 𝒕𝒐 {pos}
🎵 𝑶𝒏 𝒓𝒆𝒒𝒖𝒆𝒔𝒕 {m.from_user.mention}**
""",
                )
            else:
                if Q == 720:
                    hmmm = HighQualityVideo()
                elif Q == 480:
                    hmmm = MediumQualityVideo()
                elif Q == 360:
                    hmmm = LowQualityVideo()
                await call_py.join_group_call(
                    chat_id,
                    AudioVideoPiped(dl, HighQualityAudio(), hmmm),
                    stream_type=StreamType().pulse_stream,
                )
                add_to_queue(chat_id, songname, dl, link, "Video", Q)
                await huehue.delete()
                # await m.reply_to_message.delete()
                await m.reply_text(f"""
**▶️ 𝑺𝒕𝒂𝒓𝒕𝒆𝒅 𝒑𝒍𝒂𝒚𝒊𝒏𝒈 𝒗𝒊𝒅𝒆𝒐
🎵 𝑶𝒏 𝒓𝒆𝒒𝒖𝒆𝒔𝒕 {m.from_user.mention}**
""",
                )

    else:
        if len(m.command) < 2:
            await m.reply("💫 𝑹𝒆𝒑𝒍𝒚 𝒕𝒐 𝒂𝒏 𝒗𝒊𝒅𝒆𝒐 𝒇𝒊𝒍𝒆 𝒐𝒓 𝒑𝒓𝒐𝒗𝒊𝒅𝒆 𝒔𝒐𝒎𝒆𝒕𝒉𝒊𝒏𝒈 𝒇𝒐𝒓 𝒔𝒆𝒂𝒓𝒄𝒉")
        else:
            await m.delete()
            huehue = await m.reply("🔎 𝑺𝒆𝒂𝒓𝒄𝒉𝒊𝒏𝒈...")
            query = m.text.split(None, 1)[1]
            search = ytsearch(query)
            Q = 720
            hmmm = HighQualityVideo()
            if search == 0:
                await huehue.edit("`❌ 𝑭𝒐𝒖𝒏𝒅 𝒏𝒐𝒕𝒉𝒊𝒏𝒈 `")
            else:
                songname = search[0]
                url = search[1]
                hm, ytlink = await ytdl(url)
                if hm == 0:
                    await huehue.edit(f"**𝒀𝑻𝑫𝑳 𝑬𝒓𝒓𝒐𝒓... ⚠️** \n\n`{ytlink}`")
                else:
                    if chat_id in QUEUE:
                        pos = add_to_queue(chat_id, songname, ytlink, url, "Video", Q)
                        await huehue.delete()
                        # await m.reply_to_message.delete()
                        await m.reply_text(f"""
**⃣ 𝑽𝒊𝒅𝒆𝒐𝒔 𝒂𝒅𝒅𝒆𝒅 𝒊𝒏 𝒒𝒖𝒆𝒖𝒆 𝒂𝒕 {pos}
🎵 𝑶𝒏 𝒓𝒆𝒒𝒖𝒆𝒔𝒕 {m.from_user.mention}**
""",
                        )
                    else:
                        try:
                            await call_py.join_group_call(
                                chat_id,
                                AudioVideoPiped(ytlink, HighQualityAudio(), hmmm),
                                stream_type=StreamType().pulse_stream,
                            )
                            add_to_queue(chat_id, songname, ytlink, url, "Video", Q)
                            await huehue.delete()
                            # await m.reply_to_message.delete()
                            await m.reply_text(f"""
**▶️ 𝑺𝒕𝒂𝒓𝒕𝒆𝒅 𝒑𝒍𝒂𝒚𝒊𝒏𝒈 𝒗𝒊𝒅𝒆𝒐
🎵 𝑶𝒏 𝒓𝒆𝒒𝒖𝒆𝒔𝒕 {m.from_user.mention}**
""",
                            )
                        except Exception as ep:
                            await huehue.edit(f"`{ep}`")


@Client.on_message(commandpro([".playfrom", "!playfrom", "/playfrom", "PF", "playfrom"]))
@errors
@sudo_users_only
async def playfrom(client, m: Message):
    chat_id = m.chat.id
    if len(m.command) < 2:
        await m.reply(
            f"**USE:** \n`!playfrom [chat_id/group_username]`"
        )
    else:
        args = m.text.split(maxsplit=1)[1]
        if ";" in args:
            chat = args.split(";")[0]
            limit = int(args.split(";")[1])
        else:
            chat = args
            limit = 10
            lmt = 9
        await m.delete()
        hmm = await m.reply(f"**🔎 𝑭𝒆𝒕𝒄𝒉𝒊𝒏𝒈 {limit} 𝒓𝒂𝒏𝒅𝒐𝒎 𝒔𝒐𝒏𝒈𝒔 𝒇𝒓𝒐𝒎 {chat}**")
        try:
            async for x in bot.search_messages(chat, limit=limit, filter="audio"):
                location = await x.download()
                if x.audio.title:
                    songname = x.audio.title[:30] + "..."
                else:
                    songname = x.audio.file_name[:30] + "..."
                link = x.link
                if chat_id in QUEUE:
                    add_to_queue(chat_id, songname, location, link, "Audio", 0)
                else:
                    await call_py.join_group_call(
                        chat_id,
                        AudioPiped(location),
                        stream_type=StreamType().pulse_stream,
                    )
                    add_to_queue(chat_id, songname, location, link, "Audio", 0)
                    # await m.reply_to_message.delete()
                    await m.reply_text(f"""
**▶️ 𝑺𝒕𝒂𝒓𝒕𝒆𝒅 𝒑𝒍𝒂𝒚𝒊𝒏𝒈 𝒔𝒐𝒏𝒈𝒔 𝒇𝒓𝒐𝒎 {chat}
🎵 𝑶𝒏 𝒓𝒆𝒒𝒖𝒆𝒔𝒕 {m.from_user.mention}**
""",
                    )
            await hmm.delete()
            await m.reply(
                f"➕ 𝑨𝒅𝒅𝒊𝒏𝒈 {lmt} 𝒔𝒐𝒏𝒈𝒔 𝒊𝒏𝒕𝒐 𝒒𝒖𝒆𝒖𝒆\n𝒄𝒍𝒊𝒄𝒌 `!playlist` 𝒕𝒐 𝒗𝒊𝒆𝒘 𝒑𝒍𝒂𝒚𝒍𝒊𝒔𝒕**"
            )
        except Exception as e:
            await hmm.edit(f"**𝑬𝒓𝒓𝒐𝒓....** \n`{e}`")


@Client.on_message(commandpro([".playlist", "/playlist", "!playlist", "PY", "playlist", "/queue"]))
@errors
@sudo_users_only
async def playlist(client, m: Message):
    chat_id = m.chat.id
    if chat_id in QUEUE:
        chat_queue = get_queue(chat_id)
        if len(chat_queue) == 1:
            await m.delete()
            await m.reply(
                f"**🎵 𝑵𝒐𝒘 𝑷𝒍𝒂𝒚𝒊𝒏𝒈** \n[{chat_queue[0][0]}]({chat_queue[0][2]}) | `{chat_queue[0][3]}`",
                disable_web_page_preview=True,
            )
        else:
            QUE = f"**🎵 𝑵𝒐𝒘 𝑷𝒍𝒂𝒚𝒊𝒏𝒈** \n[{chat_queue[0][0]}]({chat_queue[0][2]}) | `{chat_queue[0][3]}` \n\n**⏯️ 𝑸𝒖𝒆𝒖𝒆 𝑳𝒊𝒔𝒕**"
            l = len(chat_queue)
            for x in range(1, l):
                hmm = chat_queue[x][0]
                hmmm = chat_queue[x][2]
                hmmmm = chat_queue[x][3]
                QUE = QUE + "\n" + f"**#{x}** - [{hmm}]({hmmm}) | `{hmmmm}`\n"
            await m.reply(QUE, disable_web_page_preview=True)
    else:
        await m.reply("**❌ 𝑫𝒐𝒆𝒔𝒏'𝒕 𝒑𝒍𝒂𝒚 𝒂𝒏𝒚𝒕𝒉𝒊𝒏𝒈**")
