from datetime import datetime

from aiogram.filters import StateFilter, Text
from aiogram.fsm.context import FSMContext
from aiogram import Router, F
from aiogram.fsm.state import default_state
from aiogram.types import (CallbackQuery, Message)

from models.methods.insert import InsertInto
from states.states import FSMemploee
from keyboards.keyboards_utils import create_inline_kb

from lexicon.lexicon_ru import LEXICON_RU, TABLES
from filters.language_filter import CheckLenRowFilter, CheckUniqueFilter, CheckNameFilter, CheckDateFilter, \
    CheckIsdigitFilter
from models.methods.select import get_employee, information_about_employee, get_positions, get_duration, get_cityes, \
    get_list_employees
from models.methods.update import update_employee

router: Router = Router()


# запрашиваем фамилию или ID сотрудника
@router.callback_query(StateFilter(FSMemploee.upd_dismissal_action), Text(text=['dismissal_employee']))
@router.callback_query(~StateFilter(default_state), Text(text=['dismissal_back_to_name_emp']))
async def process_start_dismissal(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text=LEXICON_RU['dismissal_employee']['name_employee'],
                                     reply_markup=create_inline_kb('back_to_update_emp_actions', 'cancel_all', width=1))

    await state.set_state(FSMemploee.dis_name_emp)
    await callback.answer(text=LEXICON_RU['callback.answers']['go'])
    print(await state.get_state())
    print(await state.get_data())
#_________________________________


#_________________________________
# получаем значение и ищем сотрудника, выводим найденные варианты
@router.message(StateFilter(FSMemploee.dis_name_emp))
async def process_dis_finding_emp(message: Message, state: FSMContext):
    if get_employee(message.text):
        await message.answer(text=LEXICON_RU['dismissal_employee']['choose_emp'],
                             reply_markup=create_inline_kb('dismissal_back_to_name_emp', 'cancel_all',
                                                           width=1, **get_employee(message.text)))
        await state.update_data(names=get_employee(message.text))

    else:
        await message.answer(text=LEXICON_RU['dismissal_employee']['repeat'],
                             reply_markup=create_inline_kb('cancel_all'))
    print(await state.get_state())
    print(await state.get_data())
#_________________________________



# Выводим выбор текущих позиций из таблицы
@router.callback_query(StateFilter(FSMemploee.dis_name_emp))
@router.callback_query(~StateFilter(default_state), Text(text=['back_to_add_date_dismissal']))
async def process_add_date_of_dismissal(callback: CallbackQuery, state: FSMContext):
    if callback.data != 'back_to_add_date_dismissal':
        await state.update_data(employee_id=callback.data)
    data = await state.get_data()
    await callback.message.edit_text(text=LEXICON_RU['dismissal_employee']['add_date']+data['names'][data['employee_id']],
                                     reply_markup=create_inline_kb('dismissal_back_to_name_emp', 'cancel_all',
                                                                   width=1))
    await state.set_state(FSMemploee.dis_approve_date)
    print(await state.get_state())
    print(await state.get_data())
#____________________



# принимаем дату увольнения сотрудника и предлагаем подтвердить изменение
@router.message(StateFilter(FSMemploee.dis_approve_date), F.content_type == 'text', CheckDateFilter())
async def process_approve_date_of_dismissal(message: Message, state: FSMContext, new_date: str):
    await state.update_data(date_of_dismissal=new_date)
    data = await state.get_data()
    await message.answer(text=f'Подтвердите указанную ранее информацию:\n'
                              f'ФИО - {data["names"][data["employee_id"]]}\n'
                              f'Дата увольнения - {datetime.strptime(data["date_of_dismissal"], "%Y.%m.%d").strftime("%d.%m.%Y")}',
                         reply_markup=create_inline_kb('yes', 'no', 'back_to_add_date_dismissal', 'cancel_all', width=1))
    await state.set_state(FSMemploee.dis_approve_answer)
    print(await state.get_state())
    print(await state.get_data())



# Записывает дату увольнения сотрудника в таблицу
@router.callback_query(StateFilter(FSMemploee.dis_approve_answer))
async def process_dis_approve_date_of_employment(callback: CallbackQuery, state: FSMContext):
    if callback.data == 'yes':
        update_employee(column='date_of_dismissal', new_value=await state.get_data())
        await callback.answer(text=LEXICON_RU['callback.answers']['finish_yes'], show_alert=True)
    else:
        await callback.answer(text=LEXICON_RU['callback.answers']['finish_no'], show_alert=True)

    await callback.message.answer(text=LEXICON_RU['start'], reply_markup=create_inline_kb(width=1, **TABLES))
    await state.clear()
#_________________________________













