from datetime import datetime
from aiogram.filters import StateFilter, Text
from aiogram.fsm.context import FSMContext
from aiogram import Router
from aiogram.fsm.state import default_state
from aiogram.types import (CallbackQuery, Message)
from states.states import FSMemploee, FSMpositions
from keyboards.keyboards_utils import create_inline_kb

from lexicon.lexicon_ru import LEXICON_RU
from models.methods.select import get_employee, information_about_employee, get_position_history

router: Router = Router()


# запрашиваем фамилию или ID сотрудника
@router.callback_query(StateFilter(FSMpositions.choose_action), Text(text=['positions_history']))
@router.callback_query(~StateFilter(default_state), Text(text=['pos_back_to_name_emp']))
async def process_start_show_positions(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text=LEXICON_RU['position_history']['name_employee'],
                                     reply_markup=create_inline_kb('back_to_position_actions', 'cancel_all', width=1))

    await state.set_state(FSMpositions.name_employee)
    await callback.answer(text=LEXICON_RU['callback.answers']['go'])
    print(await state.get_state())
    print(await state.get_data())


# получаем значение и ищем сотрудника, выводим найденные варианты
@router.message(StateFilter(FSMpositions.name_employee))
async def process_finding_emp(message: Message, state: FSMContext):
    if get_employee(message.text):
        await message.answer(text=LEXICON_RU['position_history']['choose_emp_from_list'],
                             reply_markup=create_inline_kb('pos_back_to_name_emp', 'cancel_all',
                                                           width=1, **get_employee(message.text)))
    else:
        await message.answer(text=LEXICON_RU['position_history']['repeat'],
                             reply_markup=create_inline_kb('cancel_all'))
    print(await state.get_state())
    print(await state.get_data())


# Выводим список должностей с датой их изменения текущих позиций из таблицы
@router.callback_query(StateFilter(FSMpositions.name_employee))
async def process_upd_actions(callback: CallbackQuery, state: FSMContext):
    await state.update_data(employee_id=callback.data)

    positions: dict[datetime, str] = get_position_history(callback.data)
    await callback.message.edit_text(text='\n'.join([f'{k.strftime("%d.%m.%Y")} - {v}' for k, v in positions.items()]),
                                     reply_markup=create_inline_kb('pos_back_to_name_emp', 'cancel_all',
                                                                   width=1,))
    await state.set_state(FSMpositions.show_position_history)
    print(await state.get_state())
    print(await state.get_data())


#