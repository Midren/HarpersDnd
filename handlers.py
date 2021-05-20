import typing as t

import telebot

from bot import bot
from harper import (Harper, add_harper, all_harper_ids, change_harper_name, get_harper, get_name,
                    is_present, remove_harper)


def is_harper(message: telebot.types.Message) -> bool:
    if not is_present(message.from_user.id):
        bot.reply_to(
            message,
            'Hello!\nYou are not part of the network. To join network write /join <b>Name</b>')
        return False
    return True


def send_text_message_from(harper: Harper, msg: str):
    for harper_id in filter(lambda harper_id: harper_id != harper.chat_id, all_harper_ids()):
        bot.send_message(harper_id, msg)


def prepend_name(name: str, msg: t.Optional[str]) -> str:
    return f"<b>{name}</b>\n{msg if msg is not None else ''}"


def send_message_from(harper: Harper, msg: telebot.types.Message):
    # for harper_id in filter(lambda harper_id: harper_id != harper.chat_id, all_harper_ids()):
    for harper_id in all_harper_ids():
        bot.send_chat_action(harper_id, 'typing')
        if msg.photo is not None:
            bot.send_photo(harper_id,
                           photo=msg.photo[0].file_id,
                           caption=prepend_name(harper.name, msg.html_caption),
                           reply_to_message_id=msg.reply_to_message)
        elif msg.video is not None:
            bot.send_video(harper_id,
                           data=msg.video[0].file_id,
                           caption=prepend_name(harper.name, msg.html_caption),
                           reply_to_message_id=msg.reply_to_message)
        elif msg.sticker is not None:
            bot.send_sticker(harper_id,
                             data=msg.sticker.file_id,
                             reply_to_message_id=msg.reply_to_message)
        elif msg.document is not None:
            bot.send_document(harper_id,
                              data=msg.document.file_id,
                              reply_to_message_id=msg.reply_to_message)
        else:
            bot.send_message(harper_id,
                             prepend_name(harper.name, msg.html_text),
                             reply_to_message_id=msg.reply_to_message)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message: telebot.types.Message):
    is_harper(message)


@bot.message_handler(commands=['join'])
def join_network(message: telebot.types.Message):
    usr_id = message.from_user.id
    if not is_present(usr_id):
        name = " ".join(message.text.split(' ')[1:]).strip()
        if len(name) == 0:
            bot.reply_to(message, 'Name cannot be blank. To join network write /join <b>Name</b>')
            return
        harper = Harper(0, name, message.from_user.id)
        add_harper(harper)
        bot.reply_to(message, f"Hello {name}! Welcome in the network")
        send_text_message_from(harper, f"{name} has joined the network")
    else:
        bot.reply_to(message, "You are already part of network! To change nick /rename <b>Name</b>")


@bot.message_handler(commands=['leave'])
def leave_network(message: telebot.types.Message):
    if not is_harper(message):
        return
    remove_harper(message.from_user.id)
    bot.reply_to(message, "You have successfully left the Network!")


@bot.message_handler(commands=['rename'])
def change_nick_name(message: telebot.types.Message):
    if not is_harper(message):
        return

    name = " ".join(message.text.split(' ')[1:]).strip()
    if len(name) == 0:
        bot.reply_to(message, 'Name cannot be blank. To change nick /rename <b>Name</b>')
        return
    change_harper_name(message.from_user.id, name)
    bot.reply_to(message, f'You changed your "<i>name</i>" to {name}!')


@bot.message_handler(func=lambda m: True,
                     content_types=['photo', 'video', 'document', 'text', 'sticker'])
def echo_all(message: telebot.types.Message):
    if not is_harper(message):
        return
    if harper := get_harper(message.from_user.id):
        send_message_from(harper, message)
