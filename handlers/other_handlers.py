from aiogram.filters import StateFilter
from aiogram.fsm.state import default_state
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from aiogram import Router
from lexicon.lexicon_ru import LEXICON_RU
from keyboards.keyboards_utils import create_inline_kb
from aiogram.utils.keyboard import ReplyKeyboardBuilder

router: Router = Router()



# Этот хендлер ловит сообщения не обработанные всеми остальными хендлерами
@router.message(~StateFilter(default_state))
async def fault_handler(message: Message):
    await message.answer(text=LEXICON_RU['fault_text'], reply_markup=create_inline_kb('cancel_all', width=1,))
    LEXICON_RU['fault_text'] = 'Введенное значение не принято, попробуйте еще раз'



@router.message(StateFilter(default_state))
async def last_handler(message: Message):
    await message.answer(text=LEXICON_RU['last'])

