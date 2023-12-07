import aiogram
import logging
from aiogram.types.reply_keyboard import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton
from aiogram.types.inline_keyboard import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram import types, executor, Dispatcher, Bot

def log(message):
    print("<!------!>")
    from datetime import datetime
    print(datetime.now())
    print("Сообщение от {0} {1} (id = {2}) \n {3}".format(message.from_user.first_name,
                                                              message.from_user.last_name,
                                                              str(message.from_user.id), message.text))


logging.basicConfig()

bot = aiogram.Bot("TOKEN") # Токен бота
storage = MemoryStorage()
dp = aiogram.Dispatcher(bot, storage=storage)


@dp.message_handler(commands=["start"])
async def start_handler(message: aiogram.types.Message):
        markup = ReplyKeyboardMarkup(resize_keyboard=True) # Кнопки на які натискає користувач
        btn1 = KeyboardButton('Поповнити свою картку')
        btn2 = KeyboardButton('Переказати на картку')
        btn3 = KeyboardButton('інші платежі')
        btn4 = KeyboardButton('історія платежів')
        markup.add(btn1).add(btn2).add(btn3, btn4)
        await bot.send_message(message.chat.id, "Ваш баланс: - 0 UAH(Баланс завантажується, очікуйте)", reply_markup=markup) # Фейк Особистий Кабінет
        log(message)



@dp.message_handler(content_types=['text'])
async def get_text_messages(message: types.Message):
    if message.text == 'Поповнити свою картку':
      await bot.send_message(message.from_user.id, '❌Очікуйте поки баланс завантажиться') # Відповідь після натиску на кнопкиі
    if message.text == 'Переказати на картку':
      await bot.send_message(message.from_user.id, '❌Очікуйте поки баланс завантажиться')
    if message.text == 'інші платежі':
      await bot.send_message(message.from_user.id, '❌Очікуйте поки баланс завантажиться')
    if message.text == 'історія платежів':
      await bot.send_message(message.from_user.id, '❌Очікуйте поки баланс завантажиться')









aiogram.executor.start_polling(dp, skip_updates=True)