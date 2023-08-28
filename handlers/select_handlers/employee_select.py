from aiogram.filters import StateFilter, Text
from aiogram.fsm.context import FSMContext
from aiogram import Router
from aiogram.fsm.state import default_state
from aiogram.types import (CallbackQuery, Message)
from states.states import FSMemploee
from keyboards.keyboards_utils import create_inline_kb

from lexicon.lexicon_ru import LEXICON_RU
from models.methods.select import get_employee, information_about_employee

router: Router = Router()


# запрашиваем фамилию или ID сотрудника
@router.callback_query(StateFilter(FSMemploee.select_emp_actions), Text(text=['employee_select']))
@router.callback_query(~StateFilter(default_state), Text(text=['sel_back_to_name_emp']))
async def process_start_sel_employee(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text=LEXICON_RU['select_employee']['name_employee'],
                                     reply_markup=create_inline_kb('back_to_select_emp_actions', 'cancel_all', width=1))

    await state.set_state(FSMemploee.sel_name_emp)
    await callback.answer(text=LEXICON_RU['callback.answers']['go'])
    print(await state.get_state())
    print(await state.get_data())


# получаем значение и ищем сотрудника, выводим найденные варианты
@router.message(StateFilter(FSMemploee.sel_name_emp))
async def process_upd_finding_emp(message: Message, state: FSMContext):
    if get_employee(name_emp=message.text, show_dismissed=True):
        await message.answer(text=LEXICON_RU['select_employee']['choose_emp_from_list'],
                             reply_markup=create_inline_kb('sel_back_to_name_emp', 'cancel_all',
                                                           width=1, **get_employee(name_emp=message.text, show_dismissed=True)))
    else:
        await message.answer(text=LEXICON_RU['select_employee']['repeat'],
                             reply_markup=create_inline_kb('cancel_all'))
    print(await state.get_state())
    print(await state.get_data())


# Выводим выбор текущих позиций из таблицы
@router.callback_query(StateFilter(FSMemploee.sel_name_emp))
async def process_upd_actions(callback: CallbackQuery, state: FSMContext):
    await state.update_data(employee_id=callback.data)
    employee_inf = information_about_employee(await state.get_data())
    await callback.message.edit_text(text='\n'.join(employee_inf.values()),
                                     reply_markup=create_inline_kb('sel_back_to_name_emp', 'cancel_all',
                                                                   width=1,))
    await state.set_state(FSMemploee.sel_show_emp_inf)
    print(await state.get_state())
    print(await state.get_data())


#