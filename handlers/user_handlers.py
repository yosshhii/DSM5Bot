from asyncio import sleep

from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.filters import CommandStart

from lexicon.lexicon import LEXICON_RU
from data.users_data import users
from keyboards.keyboards import yes_no_kb, choice_kb
from service.service import get_next_test_question, get_next_diagnostic_question

router: Router = Router()


@router.message(CommandStart())
async def process_start_command(message: Message):
    users[message.from_user.id] = {
        'test_question': get_next_test_question(),
        'diagnostic_question': get_next_diagnostic_question(),
        'test': 0,
        'frequency': 0,
        'intensity': 0,
    }

    await message.answer(text=LEXICON_RU['/start'])
    await sleep(1.5)
    await message.answer(text=next(users[message.from_user.id]['test_question']),
                         reply_markup=yes_no_kb)


@router.message(F.text.in_((LEXICON_RU['yes'], LEXICON_RU['no'])))
async def test_answer(message: Message):
    if message.text == LEXICON_RU['yes']:
        users[message.from_user.id]['test'] += 1
    try:
        await message.answer(text=next(users[message.from_user.id]['test_question']))
    except StopIteration:
        if users[message.from_user.id]['test'] >= 2:
            await message.answer(text=LEXICON_RU['correct_test'],
                                 reply_markup=ReplyKeyboardRemove())
            await sleep(1.5)
            await message.answer(text=LEXICON_RU['message_after_correct_test'])
            await sleep(1.5)
            await message.answer(text=next(users[message.from_user.id]['diagnostic_question']),
                                 reply_markup=choice_kb)
            users[message.from_user.id]['question_counter'] = 0
        else:
            await message.answer(text=LEXICON_RU['incorrect_test'],
                                 reply_markup=ReplyKeyboardRemove())


@router.message(F.text.in_({'0', '1', '2', '3', '4'}))
async def diagnostic_answer(message: Message):
    try:
        if users[message.from_user.id]['question_counter'] % 2 == 0:
            users[message.from_user.id]['frequency'] += int(message.text)
        else:
            users[message.from_user.id]['intensity'] += int(message.text)
        users[message.from_user.id]['question_counter'] += 1
        await message.answer(text=next(users[message.from_user.id]['diagnostic_question']))
    except StopIteration:
        await message.answer(text=LEXICON_RU['diagnostics_completed'],
                             reply_markup=ReplyKeyboardRemove())
        await sleep(3.5)
        frequency = users[message.from_user.id]['frequency']
        intensity = users[message.from_user.id]['intensity']
        question_amount = users[message.from_user.id]['question_counter'] // 2
        if (intensity / question_amount > 2) and (frequency / question_amount > 1):
            await message.answer(text=LEXICON_RU['correct_diagnostics'])
            await sleep(2)
            await message.answer(text=LEXICON_RU['recommendations'])
        else:
            await message.answer(text=LEXICON_RU['incorrect_diagnostics'])
        await sleep(2)
        await message.answer(text=LEXICON_RU['great_speech'])


@router.message()
async def process_any_message(message: Message):
    await message.answer(text=LEXICON_RU['press_buttons'])
