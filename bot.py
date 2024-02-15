BOT_TOKEN = '6562032520:AAECGlI-Y_T6ugZMOdxYNCXYjjnnQJ1MISk'
import asyncio
import logging

from aiogram import F, Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import CommandStart, Command

bot = Bot(token = BOT_TOKEN)
dp = Dispatcher()
global language
global pl

language = ""
pl = ""

books = [
    {"title": "Java. Руководство для начинающих, 9-е изд.", "author": "Герберт Шилдт", "language": "Русский 🇷🇺", "programming_language": "Java", "link": "https://t.me/c/1932166356/2262"},
    {"title": "Java from EPAM: Учебно-методическое пособие, 2-е изд.", "author": "Блинов И.Н., Романчик В.С.", "language": "Русский 🇷🇺", "programming_language": "Java", "link": "https://t.me/c/1932166356/1945"},
    {"title": "Java за неделю. Вводный курс", "author": "Валерий Яценков", "language": "Русский 🇷🇺", "programming_language": "Java", "link": "https://t.me/c/1932166356/1897"},
]

class ButtonText:
    LANGUAGE = "Choose book language📚"
    PL = "Choose topic🤖"
    FIND = "Find books🔎"
    RU = "Русский 🇷🇺"
    EN = "English 🇬🇧"
    CPP = "C++"
    PY = "Python"
    JS = "JavaScript"
    JAVA = "Java"
    SQL = "SQL"
    HCSS = "HTML + CSS"

def filter_buttons():
    button_language = KeyboardButton(text=ButtonText.LANGUAGE)
    button_pl = KeyboardButton(text=ButtonText.PL)
    button_find = KeyboardButton(text=ButtonText.FIND)
    button_first_row = [button_language, button_pl]
    button_second_row = [button_find]
    markup = ReplyKeyboardMarkup(
        keyboard = [button_first_row, button_second_row],
        resize_keyboard = True,
    )
    return markup

def language_buttons():
    button_ru = KeyboardButton(text=ButtonText.RU)
    button_en = KeyboardButton(text=ButtonText.EN)
    button_first_row = [button_ru, button_en]
    markup = ReplyKeyboardMarkup(
        keyboard = [button_first_row],
        resize_keyboard = True,
        one_time_keyboard = True,
    )
    return markup

def pl_buttons():
    button_cpp = KeyboardButton(text=ButtonText.CPP)
    button_py = KeyboardButton(text=ButtonText.PY)
    button_js = KeyboardButton(text=ButtonText.JS)
    button_java = KeyboardButton(text=ButtonText.JAVA)
    button_sql = KeyboardButton(text=ButtonText.SQL)
    button_hcss = KeyboardButton(text=ButtonText.HCSS)
    button_first_row = [button_cpp, button_py]
    button_second_row = [button_js, button_java]
    button_third_row = [button_sql, button_hcss]
    markup = ReplyKeyboardMarkup(
        keyboard = [button_first_row, button_second_row, button_third_row],
        resize_keyboard = True,
        one_time_keyboard = True,
    )
    return markup

@dp.message(CommandStart())
async def handle_start(message: types.Message):
    await message.answer(
        text=f"Hello, {message.from_user.full_name}!. Use filter to find books! Use /menu to check commands.",
        )

@dp.message(Command("menu"))
async def handle_menu(message: types.Message):
    await message.answer(
        text = "Menu options:",
        reply_markup=filter_buttons(),
        )

@dp.message(F.text == ButtonText.LANGUAGE)
@dp.message(Command("language"))
async def handle_language(message: types.Message):
    await message.answer(
        text="Choose book language: ",
        reply_markup=language_buttons(),
    )

@dp.message(F.text == ButtonText.PL)
@dp.message(Command("topic"))
async def handle_topic(message: types.Message):
    await message.answer(
        text="Choose interesting topic: ",
        reply_markup=pl_buttons(),
    )

@dp.message(F.text == ButtonText.RU)
@dp.message(F.text == ButtonText.EN)
async def handle_language_choice(message: types.Message):
    language = message.text
    await message.answer(text=f"Your language is: {language}")
    await handle_menu(message)

@dp.message(F.text == ButtonText.CPP)
@dp.message(F.text == ButtonText.PY)
@dp.message(F.text == ButtonText.JS)
@dp.message(F.text == ButtonText.JAVA)
@dp.message(F.text == ButtonText.HCSS)
@dp.message(F.text == ButtonText.SQL)
async def handle_pl_choice(message: types.Message):
    pl = message.text
    await message.answer(f"Your topic is: {pl}")
    await handle_menu(message)

def filter_books(language="", pl=""):
    filtered_books = []
    for book in books:
        if (not language or book["language"].lower() == language.lower()) and (not pl or book["programming_language"].lower() == pl.lower()):
            filtered_books.append(f"{book['title']} {book['author']} {book['link']} \n")
    return filtered_books

@dp.message(F.text == ButtonText.FIND)
async def filter_handler(message: types.Message):
    books = filter_books()
    if books:
        await message.answer("\n".join(books))
    else:
        await message.answer("Sorry, no books found for the selected language and topic.")

@dp.message()
async def handle_unknown(message: types.Message):
    await message.answer("Sorry, I can't speak elvin :c")

async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())