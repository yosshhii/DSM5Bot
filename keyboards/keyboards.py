from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from lexicon.lexicon import LEXICON_RU

button_yes = KeyboardButton(text=LEXICON_RU['yes'])
button_no = KeyboardButton(text=LEXICON_RU['no'])

yes_no_kb_builder = ReplyKeyboardBuilder()

yes_no_kb_builder.row(button_yes, button_no, width=2)

yes_no_kb: ReplyKeyboardMarkup = yes_no_kb_builder.as_markup(
    resize_keyboard=True,
)


button_0 = KeyboardButton(text="0")
button_1 = KeyboardButton(text="1")
button_2 = KeyboardButton(text="2")
button_3 = KeyboardButton(text="3")
button_4 = KeyboardButton(text="4")

choice_kb =  ReplyKeyboardMarkup(keyboard=[[button_0, button_1, button_2],
                                           [button_3, button_4]],
                                 resize_keyboard=True)
