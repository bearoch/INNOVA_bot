from datetime import datetime
from aiogram.filters import StateFilter, Text
from aiogram.fsm.context import FSMContext
from aiogram import Router
from aiogram.fsm.state import default_state
from aiogram.types import (CallbackQuery, Message)
from states.states import FSMsalary
from keyboards.keyboards_utils import create_inline_kb

from lexicon.lexicon_ru import LEXICON_RU
from models.methods.select import get_employee, get_salary_history

router: Router = Router()


# запрашиваем фамилию или ID сотрудника
@router.callback_query(StateFilter(FSMsalary.choose_action), Text(text=['salary_history']))
@router.callback_query(~StateFilter(default_state), Text(text=['salary_back_to_name_emp']))
async def process_start_show_salary_history(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text=LEXICON_RU['salary_history']['name_employee'],
                                     reply_markup=create_inline_kb('back_to_salary_actions', 'cancel_all', width=1))

    await state.set_state(FSMsalary.name_employee)
    await callback.answer(text=LEXICON_RU['callback.answers']['go'])
    print(await state.get_state())
    print(await state.get_data())


# получаем значение и ищем сотрудника, выводим найденные варианты
@router.message(StateFilter(FSMsalary.name_employee))
async def process_finding_emp(message: Message, state: FSMContext):
    if get_employee(message.text):
        await message.answer(text=LEXICON_RU['salary_history']['choose_emp_from_list'],
                             reply_markup=create_inline_kb('salary_back_to_name_emp', 'cancel_all',
                                                           width=1, **get_employee(message.text)))
    else:
        await message.answer(text=LEXICON_RU['salary_history']['repeat'],
                             reply_markup=create_inline_kb('cancel_all'))
    print(await state.get_state())
    print(await state.get_data())


# Выводим список зарплат сотрудника, с датой их изменения из таблицы
@router.callback_query(StateFilter(FSMsalary.name_employee))
async def show_salary_history(callback: CallbackQuery, state: FSMContext):
    salary: dict[datetime, str] = get_salary_history(callback.data)
    await callback.message.edit_text(text=get_employee(callback.data)[callback.data] + ':\n'
                                          + '\n'.join([f'{k.strftime("%d.%m.%Y")} - {v}' for k, v in salary.items()]),
                                     reply_markup=create_inline_kb('salary_back_to_name_emp', 'cancel_all',
                                                                   width=1,))
    await state.set_state(FSMsalary.show_salary_history)
    print(await state.get_state())
    print(await state.get_data())


