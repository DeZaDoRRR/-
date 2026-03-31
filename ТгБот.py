import telebot
from telebot import types
import random

TOKEN = ""
bot = telebot.TeleBot(TOKEN)

choices = ["Камінь", "Ножиці", "Папір"]
scores = {}
win_streak = {}
guess_number = {}
calc_mode = {}

# Список фильмов
films = {
    "Інтерстеллар": "Рік: 2014\nЖанр: фантастика\nФільм про подорож у космос для порятунку людства.",
    "Аватар": "Рік: 2009\nЖанр: фантастика\nІсторія про планету Пандора та її мешканців.",
    "Титанік": "Рік: 1997\nЖанр: драма\nЛюбовна історія на кораблі Титанік."
}

# (игры + фильмы + калькулятор)
def get_keyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add("Камінь", "Ножиці", "Папір")
    keyboard.add("Вгадай число", "Однорукий бандит")
    keyboard.add("Кинути кубик")
    keyboard.add("Інтерстеллар", "Аватар")
    keyboard.add("Титанік")
    keyboard.add("Калькулятор часу")
    keyboard.add("Рахунок", "Вийти")
    return keyboard

# /start
@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    if user_id not in scores:
        scores[user_id] = {"user": 0, "bot": 0}
        win_streak[user_id] = 0
    bot.send_message(
        message.chat.id,
        "Вибери гру або фільм:",
        reply_markup=get_keyboard()
    )

# Кнопка калькулятора
@bot.message_handler(func=lambda message: message.text == "Калькулятор часу")
def start_calc(message):
    user_id = message.from_user.id
    calc_mode[user_id] = True
    bot.send_message(message.chat.id, "Режим калькулятора активний! Пиши через :, наприклад: 1:30 + 2:15")

# Калькулятор времени
@bot.message_handler(func=lambda message: True)
def calculator(message):
    user_id = message.from_user.id


    if not calc_mode.get(user_id):
        return

    text = message.text.replace(" ", "")

    # Проверка формата
    if ":" not in text or "+" not in text:
        bot.send_message(message.chat.id, "Напиши часи і хвилини через :, наприклад: 1:30 + 2:15")
        return

    try:
        parts = text.split("+")
        total_minutes = 0

        for part in parts:
            if ":" in part:
                hours, minutes = part.split(":")
                total_minutes += int(hours) * 60 + int(minutes)
            else:
                bot.send_message(message.chat.id, "Помилка формату 😅 Пиши через :, наприклад: 1:30 + 2:15")
                return

        hours = total_minutes // 60
        minutes = total_minutes % 60

        bot.send_message(message.chat.id, f"⏱ Результат: {hours} год {minutes} хв")

    except:
        bot.send_message(message.chat.id, "Помилка 😅 Перевір формат: 1:30 + 2:15")

# Рахунок
@bot.message_handler(func=lambda message: message.text == "Рахунок")
def show_score(message):
    user_id = message.from_user.id
    if user_id in scores:
        bot.send_message(
            message.chat.id,
            f"Твій рахунок:\nТи: {scores[user_id]['user']}\nБот: {scores[user_id]['bot']}\nСерія перемог: {win_streak[user_id]}"
        )

# Камінь-Ножиці-Папір
@bot.message_handler(func=lambda message: message.text in choices)
def play_rps(message):
    user_id = message.from_user.id
    user_choice = message.text
    bot_choice = random.choice(choices)

    if user_choice == bot_choice:
        result = "Нічия 🤝"
        win_streak[user_id] = 0
    elif (user_choice == "Камінь" and bot_choice == "Ножиці") or \
         (user_choice == "Ножиці" and bot_choice == "Папір") or \
         (user_choice == "Папір" and bot_choice == "Камінь"):
        result = "Ти виграв 🏆"
        scores[user_id]["user"] += 1
        win_streak[user_id] += 1
    else:
        result = "Бот виграв 😢"
        scores[user_id]["bot"] += 1
        win_streak[user_id] = 0

    bot.send_message(
        message.chat.id,
        f"Ти обрав: {user_choice}\nБот обрав: {bot_choice}\n\n{result}",
        reply_markup=get_keyboard()
    )

# Вгадай число
@bot.message_handler(func=lambda message: message.text == "Вгадай число")
def start_guess(message):
    number = random.randint(1, 10)
    guess_number[message.chat.id] = number
    bot.send_message(
        message.chat.id,
        "Я загадав число від 1 до 10. Спробуй вгадати!"
    )

@bot.message_handler(func=lambda message: message.text.isdigit())
def guess(message):
    chat_id = message.chat.id
    if chat_id not in guess_number:
        return
    number = guess_number[chat_id]
    if int(message.text) == number:
        bot.send_message(chat_id, "Ти вгадав! 🎉", reply_markup=get_keyboard())
        del guess_number[chat_id]
    else:
        bot.send_message(chat_id, "Ні, спробуй ще 😅")

# Однорукий бандит
@bot.message_handler(func=lambda message: message.text == "Однорукий бандит")
def slot(message):
    items = ["🍒", "🍋", "⭐", "7"]
    r1 = random.choice(items)
    r2 = random.choice(items)
    r3 = random.choice(items)
    if r1 == r2 == r3:
        result = "ДЖЕКПОТ! 🎰"
    elif r1 == r2 or r2 == r3 or r1 == r3:
        result = "Майже виграв!"
    else:
        result = "Спробуй ще!"
    bot.send_message(message.chat.id, f"{r1} | {r2} | {r3}\n{result}", reply_markup=get_keyboard())

# Кинути кубик
@bot.message_handler(func=lambda message: message.text == "Кинути кубик")
def dice(message):
    number = random.randint(1, 6)
    bot.send_message(message.chat.id, f"🎲 Випало число: {number}", reply_markup=get_keyboard())

# Вийти
@bot.message_handler(func=lambda message: message.text == "Вийти")
def exit_game(message):
    user_id = message.from_user.id
    if user_id in calc_mode:
        calc_mode[user_id] = False
    bot.send_message(message.chat.id, "Дякую за гру!", reply_markup=types.ReplyKeyboardRemove())

# Фильмы
@bot.message_handler(func=lambda message: message.text in films)
def show_film_info(message):
    film = message.text
    bot.send_message(message.chat.id, f"{film}\n\n{films[film]}", reply_markup=get_keyboard())

bot.infinity_polling()