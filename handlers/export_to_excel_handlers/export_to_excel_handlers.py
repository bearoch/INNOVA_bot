from datetime import datetime

from aiogram import Router
from aiogram.filters import StateFilter, Text
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import (CallbackQuery, Message, FSInputFile)

from models.methods.export_to_excel import create_xls_file
from states.states import FSMemploee, FSMpositions, FSMsalary
from keyboards.keyboards_utils import create_inline_kb
from lexicon.lexicon_ru import LEXICON_RU

router: Router = Router()

# Выгрузить информацию о всех сотрудниках, за исключением уволенных
@router.callback_query(StateFilter(FSMemploee.select_emp_actions), Text(text=['export_all_employees']))
async def process_export_all_employees(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    print('we are here')
    address = create_xls_file('all_employs')
    print(address)
    if address:
        file = FSInputFile(address, filename=f"all_employs_{datetime.now().strftime('%d.%m.%Y_%H-%M')}.xlsx")
        await callback.message.answer_document(file, reply_markup=create_inline_kb('cancel_all_export'))
    else:
        await callback.message.edit_text(text=LEXICON_RU['select_employee']['cant_export_all_employs'],
                                         reply_markup=create_inline_kb('back_to_select_emp_actions', 'cancel_all'))


#___________________________________
# Выгрузить информацию о сотрудниках, уволенных из компании
@router.callback_query(StateFilter(FSMemploee.select_emp_actions), Text(text=['export_all_dismissal_employees']))
async def process_export_dismissal_employee(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    address = create_xls_file('dismissal')
    print(address)
    if address:
        file = FSInputFile(address, filename=f"dismissal_{datetime.now().strftime('%d.%m.%Y_%H-%M')}.xlsx")
        await callback.message.answer_document(file, reply_markup=create_inline_kb('cancel_all_export'))
    else:
        await callback.message.edit_text(text=LEXICON_RU['select_employee']['cant_export_dismissal_employs'],
                                         reply_markup=create_inline_kb('back_to_select_emp_actions', 'cancel_all'))



#___________________________________
# Выгрузить информацию о сотрудниках, находящихся на испытательном сроке
@router.callback_query(StateFilter(FSMemploee.select_emp_category), Text(text=['all_employees_on_duration_of_probation']))
async def process_export_employs_on_probation(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    address = create_xls_file('have_duration_of_probation')
    print(address)
    if address:
        file = FSInputFile(address, filename=f"employs_on_probation_{datetime.now().strftime('%d.%m.%Y_%H-%M')}.xlsx")
        await callback.message.answer_document(file, reply_markup=create_inline_kb('cancel_all_export'))
    else:
        await callback.message.edit_text(text=LEXICON_RU['select_employee']['cant_export_employs_on_probation'],
                                         reply_markup=create_inline_kb('back_select_emp_on_duration_actions', 'cancel_all'))


# Выгрузить историю должностей сотрудников
@router.callback_query(StateFilter(FSMpositions.choose_action), Text(text=['export_position_history']))
async def process_export_positions_history(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    address = create_xls_file('position_history')
    print(address)
    if address:
        file = FSInputFile(address, filename=f"dismissal_{datetime.now().strftime('%d.%m.%Y_%H-%M')}.xlsx")
        await callback.message.answer_document(file, reply_markup=create_inline_kb('cancel_all_export'))
    else:
        await callback.message.edit_text(text=LEXICON_RU['select_employee']['cant_export_position_history'],
                                         reply_markup=create_inline_kb('back_to_position_actions', 'cancel_all'))






# Выгрузить историю зарплат сотрудников
@router.callback_query(StateFilter(FSMsalary.choose_action), Text(text=['export_salary_history']))
async def process_export_salary_history(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    address = create_xls_file('salary_history')
    print(address)
    if address:
        file = FSInputFile(address, filename=f"salary_history_{datetime.now().strftime('%d.%m.%Y_%H-%M')}.xlsx")
        await callback.message.answer_document(file, reply_markup=create_inline_kb('cancel_all_export'))
    else:
        await callback.message.edit_text(text=LEXICON_RU['select_employee']['cant_export_salary_history'],
                                         reply_markup=create_inline_kb('back_to_salary_actions', 'cancel_all'))
