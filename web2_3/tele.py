import telebot
import os
from telebot import types
TOKEN = "7241355746:AAFe0f6AwuMz5OIZS4vFAiVAY4w_Tir9f6E"

COMMENTS_FILE = "comments.txt"

ADMIN_LIST = ["bkd42nd"]

bot = telebot.TeleBot(TOKEN)

def read_comments():
    with open(COMMENTS_FILE, "r", encoding="utf-8") as file:
        return file.readlines()

def write_comment(user, comment):
    with open(COMMENTS_FILE, "a", encoding="utf-8") as file:
        file.write(f"{user}: {comment}\n")

def write_all_comments(comments):
    with open(COMMENTS_FILE, "w", encoding="utf-8") as file:
        file.writelines(comments)

@bot.message_handler(commands=["start"])
def send_welcome(message):
    markup = types.InlineKeyboardMarkup()
    
    add_comment_button = types.InlineKeyboardButton("✍ Добавить комментарий", callback_data="add_comment")
    
    my_comments_button = types.InlineKeyboardButton("🗑 Удалить свои комментарии", callback_data="delete_my_comments")
    
    list_comments_button = types.InlineKeyboardButton("📄 Посмотреть список комментариев", callback_data="list_comments")

    markup.add(add_comment_button)
    markup.add(my_comments_button)
    markup.add(list_comments_button)
    
    if message.from_user.username in ADMIN_LIST:
        delete_others_button = types.InlineKeyboardButton("🗑 Удалить чужие комментарии", callback_data="delete_others_menu")
        markup.add(delete_others_button)
    
    bot.reply_to(message, "Добро пожаловать! Выберите действие:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_menu_handler(call):
    if call.data == "add_comment":
        add_comment(call)
    elif call.data == "delete_my_comments":
        delete_my_comments(call)
    elif call.data == "delete_others_menu":
        admin_delete_menu(call)
    elif call.data == "list_comments":
        list_comments(call.message)

def add_comment(call):
    bot.answer_callback_query(call.id)
    bot.send_message(call.message.chat.id, "Напишите свой комментарий:")

    bot.register_next_step_handler(call.message, process_add_comment)

def process_add_comment(message):
    user = message.from_user.username
    comment = message.text

    write_comment(user, comment)
    bot.send_message(message.chat.id, f"Комментарий от @{user} добавлен!")

def delete_my_comments(call):
    user = call.from_user.username
    comments = read_comments()
    new_comments = [c for c in comments if not c.startswith(f"{user}:")]

    if len(new_comments) == len(comments):
        bot.answer_callback_query(call.id, "У вас нет комментариев для удаления.")
    else:
        write_all_comments(new_comments)
        bot.answer_callback_query(call.id, "Все ваши комментарии удалены!")


def admin_delete_menu(call):
    bot.answer_callback_query(call.id)

    markup = types.InlineKeyboardMarkup()
    cancel_button = types.InlineKeyboardButton("Отмена", callback_data="cancel")
    markup.add(cancel_button)
    
    bot.send_message(call.message.chat.id, "Введите ник пользователя, чьи комментарии вы хотите удалить:")
    bot.register_next_step_handler(call.message, process_delete_user)

def process_delete_user(message):
    target_user = message.text
    admin_user = message.from_user.username

    if admin_user in ADMIN_LIST:
        comments = read_comments()
        new_comments = [c for c in comments if not c.startswith(f"{target_user}:")]

        if len(new_comments) == len(comments):
            bot.send_message(message.chat.id, f"Комментарии от {target_user} не найдены.")
        else:
            write_all_comments(new_comments)
            bot.send_message(message.chat.id, f"Все комментарии от @{target_user} были удалены.")
    else:
        bot.send_message(message.chat.id, "У вас нет прав для выполнения этой команды.")

def list_comments(message):
    comments = read_comments()

    if not comments:
        bot.send_message(message.chat.id, "Комментариев нет.")
    else:
        response = "Все комментарии:\n" + "".join(comments)
        bot.send_message(message.chat.id, response)

bot.polling()