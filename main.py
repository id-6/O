import pyrogram
from pyrogram import Client, filters
from pyrogram.errors import UserAlreadyParticipant, InviteHashExpired
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

import time
import os
import threading

# ===== Keep Alive Webserver =====
from flask import Flask

app = Flask('')

@app.route('/')
def home():
    return "I'm alive! 🌟"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = threading.Thread(target=run)
    t.start()

# شغل السيرفر قبل أي شي
keep_alive()

# ===== البوت =====
api_id = 18421930
api_hash = "9cf3a6feb6dfcc7c02c69eb2c286830e"

bot = Client("isici", api_id, api_hash, bot_token="5961331483:AAEH1Terp8kjpZkIr3_Hwfu5HbepC2o1CNE")

ss = "AgEZGKoATsLbXu6Bupj9kZHNJY1L9bhaimuafFQr5w-TAHcRy-zS7kDPcbW3kFjrU4o4Um4hzE0P310noLUZ6A7lhCX30VgPtyOnTVg8HxmyK8XEERyyZvoKJ3Qp8ksGX75D-4HwRA8Oz6j9YJ0japDepKSzvRqAmnUC8NuR-eOWItwxKozy8t6x8q5FTeHKNRT7tbgvmx7-88aDcNKNyVY_K-ftvNxhn7lZUJRRJAbwYyY0zjYi1Sm5NizKGmbcLGxwOQ-kiwYNr2actNZzKRmTCUszBihpcPMMhGV8oqj0y7ZiYjQ4RBFZ54PR66_RLmW3bjYRgJUygIzhKBeM0fvG7EOKxQAAAAFjUrMbAQ"

if ss is not None:
    acc = Client("myacc", api_id=api_id, api_hash=api_hash, session_string=ss)
    acc.start()
else:
    acc = None

# ===== دوال Download/Upload =====
def downstatus(statusfile,message):
    while True:
        if os.path.exists(statusfile):
            break
    time.sleep(3)      
    while os.path.exists(statusfile):
        with open(statusfile,"r") as downread:
            txt = downread.read()
        try:
            bot.edit_message_text(message.chat.id, message.id, f"__Downloaded__ : **{txt}**")
            time.sleep(10)
        except:
            time.sleep(5)

def upstatus(statusfile,message):
    while True:
        if os.path.exists(statusfile):
            break
    time.sleep(3)      
    while os.path.exists(statusfile):
        with open(statusfile,"r") as upread:
            txt = upread.read()
        try:
            bot.edit_message_text(message.chat.id, message.id, f"__Uploaded__ : **{txt}**")
            time.sleep(10)
        except:
            time.sleep(5)

def progress(current, total, message, type):
    with open(f'{message.id}{type}status.txt',"w") as fileup:
        fileup.write(f"{current * 100 / total:.1f}%")

# ===== أوامر البوت =====
@bot.on_message(filters.command(["start"]))
def send_start(client, message):
    language_code = message.from_user.language_code
    if language_code == "ar":
        welcome_message = f"**👋 مرحبًا {message.from_user.mention},\nأنا بوت حفظ المنشورات من القنوات المقيدة. ارسل لي رابط المنشور 📎**"
        reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("المطور", url="https://t.me/i77lx")]])
    else:
        welcome_message = f"**👋 Hello {message.from_user.mention},\nI'm a bot that saves posts from restricted channels. Send me the post link 📎**"
        reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("Developer", url="https://t.me/i77lx")]])

    bot.send_message(
        message.chat.id,
        welcome_message,
        reply_markup=reply_markup,
        reply_to_message_id=message.id
    )

# ===== التعامل مع الروابط =====
@bot.on_message(filters.text)
def save(client, message):
    language_code = message.from_user.language_code

    if "https://t.me/+" in message.text or "https://t.me/joinchat/" in message.text:

        if acc is None:
            bot.send_message(message.chat.id,f"**لم يتم تعيين الجلسة**", reply_to_message_id=message.id)
            return

        try:
            acc.join_chat(message.text)
            if language_code == "ar":
                bot.send_message(message.chat.id,"**لقد انضممت الى الرابط**", reply_to_message_id=message.id)
            else:
                bot.send_message(message.chat.id,"**Done join in link**", reply_to_message_id=message.id)
        except UserAlreadyParticipant:
            if language_code == "ar":
                bot.send_message(message.chat.id,"**لقد انضممت لهذهي الدردشة مسبقًا**", reply_to_message_id=message.id)
            else:
                bot.send_message(message.chat.id,"**I already joined this chat .**", reply_to_message_id=message.id)
        except InviteHashExpired:
            bot.send_message(message.chat.id,"**رابط غير صالح**", reply_to_message_id=message.id)

    elif "https://t.me/" in message.text:
        datas = message.text.split("/")
        msgid = int(datas[-1].split("?")[0])

        if "https://t.me/c/" in message.text:
            chatid = int("-100" + datas[-2])
            if acc is None:
                bot.send_message(message.chat.id,f"**لم يتم تعيين جلسة **", reply_to_message_id=message.id)
                return
            try: handle_private(message,chatid,msgid)
            except Exception as e: bot.send_message(message.chat.id,f"**خطأ** : __{e}__", reply_to_message_id=message.id)
        else:
            username = datas[-2]
            msg  = bot.get_messages(username,msgid)
            try: bot.copy_message(message.chat.id, msg.chat.id, msg.id,reply_to_message_id=message.id)
            except:
                if acc is None:
                    bot.send_message(message.chat.id,f"**لم يتم تعيين جلسة **", reply_to_message_id=message.id)
                    return
                try: handle_private(message,username,msgid)
                except Exception as e: bot.send_message(message.chat.id,f"**خطأ** : __{e}__", reply_to_message_id=message.id)

# ===== دوال خاصة بالملفات =====
def handle_private(message,chatid,msgid):
    msg  = acc.get_messages(chatid,msgid)

    if "text" in str(msg):
        bot.send_message(message.chat.id, msg.text, entities=msg.entities, reply_to_message_id=message.id)
        return

    smsg = bot.send_message(message.chat.id, '__تحميل__', reply_to_message_id=message.id)
    threading.Thread(target=lambda:downstatus(f'{message.id}downstatus.txt',smsg),daemon=True).start()
    file = acc.download_media(msg, progress=progress, progress_args=[message,"down"])
    os.remove(f'{message.id}downstatus.txt')

    threading.Thread(target=lambda:upstatus(f'{message.id}upstatus.txt',smsg),daemon=True).start()

    if "Document" in str(msg):
        try: thumb = acc.download_media(msg.document.thumbs[0].file_id)
        except: thumb = None
        bot.send_document(message.chat.id, file, thumb=thumb, caption=msg.caption, caption_entities=msg.caption_entities, reply_to_message_id=message.id, progress=progress, progress_args=[message,"up"])
        if thumb != None: os.remove(thumb)
    elif "Video" in str(msg):
        try: thumb = acc.download_media(msg.video.thumbs[0].file_id)
        except: thumb = None
        bot.send_video(message.chat.id, file, duration=msg.video.duration, width=msg.video.width, height=msg.video.height, thumb=thumb, caption=msg.caption, caption_entities=msg.caption_entities, reply_to_message_id=message.id, progress=progress, progress_args=[message,"up"])
        if thumb != None: os.remove(thumb)
    elif "Animation" in str(msg):
        bot.send_animation(message.chat.id, file, reply_to_message_id=message.id)
    elif "Sticker" in str(msg):
        bot.send_sticker(message.chat.id, file, reply_to_message_id=message.id)
    elif "Voice" in str(msg):
        bot.send_voice(message.chat.id, file, caption=msg.caption, thumb=thumb, caption_entities=msg.caption_entities, reply_to_message_id=message.id, progress=progress, progress_args=[message,"up"])
    elif "Audio" in str(msg):
        try: thumb = acc.download_media(msg.audio.thumbs[0].file_id)
        except: thumb = None
        bot.send_audio(message.chat.id, file, caption=msg.caption, caption_entities=msg.caption_entities, reply_to_message_id=message.id, progress=progress, progress_args=[message,"up"])   
        if thumb != None: os.remove(thumb)
    elif "Photo" in str(msg):
        bot.send_photo(message.chat.id, file, caption=msg.caption, caption_entities=msg.caption_entities, reply_to_message_id=message.id)

    os.remove(file)
    if os.path.exists(f'{message.id}upstatus.txt'): os.remove(f'{message.id}upstatus.txt')
    bot.delete_messages(message.chat.id,[smsg.id])

# ===== شغل البوت =====
bot.run()
