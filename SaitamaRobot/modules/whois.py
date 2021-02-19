from datetime import datetime

from pyrogram import filters
from pyrogram.types import User, Message
from pyrogram.raw import functions
from pyrogram.errors import PeerIdInvalid
from SaitamaRobot import pbot

def ReplyCheck(message: Message):
    reply_id = None

    if message.reply_to_message:
        reply_id = message.reply_to_message.message_id

    elif not message.from_user.is_self:
        reply_id = message.message_id

    return reply_id

infotext = (
    "**[{full_name}](tg://user?id={user_id})**\n"
    " * ID del Usuario: `{user_id}`\n"
    " * Nombre(s): `{first_name}`\n"
    " * Apellido(s): `{last_name}`\n"
    " * Nombre de usuario: `{username}`\n"
    " * Última vez en línea: `{last_online}`\n"
    " * Biografía: {bio}")

def LastOnline(user: User):
    if user.is_bot:
        return ""
    elif user.status == 'recently':
        return "Recientemente en línea"
    elif user.status == 'within_week':
        return "Última vez hace una semana"
    elif user.status == 'within_month':
        return "Última vez hace un mes"
    elif user.status == 'long_time_ago':
        return "Hace mucho tiempo :("
    elif user.status == 'online':
        return "Actualmente en linea"
    elif user.status == 'offline':
        return datetime.fromtimestamp(user.status.date).strftime("%a, %d %b %Y, %H:%M:%S")


def FullName(user: User):
    return user.first_name + " " + user.last_name if user.last_name else user.first_name

@pbot.on_message(filters.command('whois'))
async def whois(client, message):
    cmd = message.command
    if not message.reply_to_message and len(cmd) == 1:
        get_user = message.from_user.id
    elif len(cmd) == 1:
        get_user = message.reply_to_message.from_user.id
    elif len(cmd) > 1:
        get_user = cmd[1]
        try:
            get_user = int(cmd[1])
        except ValueError:
            pass
    try:
        user = await client.get_users(get_user)
    except PeerIdInvalid:
        await message.reply("No puedo obtener la información de este Usuario :(")
        return
    desc = await client.get_chat(get_user)
    desc = desc.description
    await message.reply_text(
            infotext.format(
                full_name=FullName(user),
                user_id=user.id,
                user_dc=user.dc_id,
                first_name=user.first_name,
                last_name=user.last_name if user.last_name else "",
                username=user.username if user.username else "",
                last_online=LastOnline(user),
                bio=desc if desc else "`No tiene configurada una Biografía.`"),
            disable_web_page_preview=True)
