import telebot
from telebot import types
import time
from langchain.memory import ConversationBufferMemory
from telegram_bot.auth_token import bot_token
from utils.preprocessing_data import txt_to_str
from llm.model.giga_chat import GiGaChatBot

# create telegram bot:
bot = telebot.TeleBot(bot_token)

# user menu memory:
user_menu = {}

# user conversation history:
user_conversation = {}

# create giga-chat bot:
giga_chat_bot = GiGaChatBot()


@bot.message_handler(commands=['start'])
def start(message):
    # create main menu:
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    info_button = types.KeyboardButton("Info")
    roles_button = types.KeyboardButton("Роли")
    prompts_button = types.KeyboardButton("Промпты")
    markup.add(info_button, roles_button, prompts_button)

    bot.send_message(message.chat.id, "Выберите действие:", reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == 'Назад')
def back_to_main_menu(message):
    start(message)


@bot.message_handler(func=lambda message: message.text == 'Роли')
def roles_menu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    copywriter_button = types.KeyboardButton("Копирайтер")
    smm_button = types.KeyboardButton("smm")
    back_button = types.KeyboardButton("Назад")
    markup.add(copywriter_button, smm_button, back_button)

    bot.send_message(message.chat.id, "Выберите опцию:", reply_markup=markup)
    user_menu[message.chat.id] = "main"


@bot.message_handler(func=lambda message: message.text == 'Копирайтер')
def create_copywriter_chat(message):
    giga_chat_bot.create_giga_model()
    bot.send_message(message.chat.id, "Копирайтер готов к работе")


@bot.message_handler(func=lambda message: message.text == 'smm')
def create_smm_bot(message):
    giga_chat_bot.create_giga_model()
    bot.send_message(message.chat.id, "smm специалист готов к работе")


bot.polling(none_stop=True)


