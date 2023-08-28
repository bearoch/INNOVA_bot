"""
В модуле реализован вывод информации о сотрудниках по категориям для кнопок:
По должностям;
По городу проживания;
По ближайшим датам рождения
"""

from datetime import datetime

from aiogram import F
from aiogram.filters import StateFilter, Text
from aiogram.fsm.context import FSMContext
from aiogram import Router
from aiogram.fsm.state import default_state
from aiogram.types import (CallbackQuery, Message)
from states.states import FSMemploee
from keyboards.keyboards_utils import create_inline_kb, create_inline_kb_arg
from models.methods.select import get_positions, get_duration, get_cityes, get_list_employees, \
    get_information_by_categoryes
from models.methods.insert import InsertInto
from lexicon.lexicon_ru import LEXICON_RU, TABLES
from filters.language_filter import CheckIsdigitFilter, CheckNameFilter, CheckDateFilter, CheckLenRowFilter, \
    CheckUniqueFilter

router: Router = Router()


# !!!!!По должностям!!!!!!!__________________________
# Выбрать должности из списка или найти нужную
@router.callback_query(StateFilter(FSMemploee.select_emp_category), Text(text=['positions_category']))
@router.callback_query(StateFilter(FSMemploee.category_position), Text(text=['searcher_position']))
async def category_by_position(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text=LEXICON_RU['select_employee']['name_position'],
                                     reply_markup=create_inline_kb('back_to_movements_emp', 'cancel_all',
                                                                   width=1,
                                                                   **get_positions(
                                                                       hold_pos=LEXICON_RU['add_row_emploee'][
                                                                           'hold_positions'])))
    await state.set_state(FSMemploee.category_position)
    print(await state.get_state())
    print(await state.get_data())


# После ввода начала названия должности выводим варианты для выбора
@router.message(StateFilter(FSMemploee.category_position))
async def category_finding_position(message: Message, state: FSMContext):
    if get_positions(name_pos=message.text):
        await message.answer(text=LEXICON_RU['select_employee']['found_positions'],
                             reply_markup=create_inline_kb('searcher_position', 'cancel_all',
                                                           width=1, **get_positions(name_pos=message.text)))
    else:
        await message.answer(text=LEXICON_RU['select_employee']['repeat_pos'],
                             reply_markup=create_inline_kb('searcher_position', 'cancel_all'))
    print(await state.get_state())
    print(await state.get_data())


@router.callback_query(StateFilter(FSMemploee.category_position))
async def information_by_position(callback: CallbackQuery, state: FSMContext):
    emp_on_pos = get_information_by_categoryes(category='positions', id=callback.data)
    if emp_on_pos:
        await callback.message.edit_text(
            text=get_positions(name_pos=callback.data)[callback.data] + ':' + '\n' + '\n'.join(emp_on_pos.values()),
            reply_markup=create_inline_kb('searcher_position', 'cancel_all'))
    else:
        await callback.message.edit_text(text=LEXICON_RU['select_employee']['repeat_search_pos'],
                                         reply_markup=create_inline_kb('searcher_position', 'cancel_all'))
    print(await state.get_state())
    print(await state.get_data())


# ____________________________________________


# !!!!!По городу проживания!!!!!!!__________________________
# Выбрать должности из списка или найти нужную
@router.callback_query(StateFilter(FSMemploee.select_emp_category), Text(text=['cities_category']))
@router.callback_query(StateFilter(FSMemploee.category_cities), Text(text=['searcher_city']))
async def category_by_cities(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text=LEXICON_RU['select_employee']['name_city'],
                                     reply_markup=create_inline_kb('back_to_movements_emp', 'cancel_all',
                                                                   width=1,
                                                                   **get_cityes('Казань')))
    await state.set_state(FSMemploee.category_cities)
    print(await state.get_state())
    print(await state.get_data())


# После ввода начала названия должности выводим варианты для выбора
@router.message(StateFilter(FSMemploee.category_cities))
async def category_finding_position(message: Message, state: FSMContext):
    if get_cityes(message.text):
        await message.answer(text=LEXICON_RU['select_employee']['found_cities'],
                             reply_markup=create_inline_kb('searcher_city', 'cancel_all',
                                                           width=1, **get_cityes(message.text)))
    else:
        await message.answer(text=LEXICON_RU['select_employee']['repeat_cities'],
                             reply_markup=create_inline_kb('searcher_city', 'cancel_all'))
    print(await state.get_state())
    print(await state.get_data())


@router.callback_query(StateFilter(FSMemploee.category_cities))
async def information_by_position(callback: CallbackQuery, state: FSMContext):
    emp_in_city = get_information_by_categoryes(category='cities', id=callback.data)
    if emp_in_city:
        await callback.message.edit_text(
            text=get_cityes(callback.data)[callback.data] + ':' + '\n' + '\n'.join(emp_in_city.values()),
            reply_markup=create_inline_kb('searcher_city', 'cancel_all'))
    else:
        await callback.message.edit_text(text=LEXICON_RU['select_employee']['repeat_search_cities'],
                                         reply_markup=create_inline_kb('searcher_city', 'cancel_all'))
    print(await state.get_state())
    print(await state.get_data())


# !!!!!По дням рождений!!!!!!!__________________________
# Выдает список дней рождений в ближайшие 30 дней
@router.callback_query(StateFilter(FSMemploee.select_emp_category), Text(text=['birthday_category']))
async def category_by_cities(callback: CallbackQuery, state: FSMContext):
    emp_birthday = get_information_by_categoryes(category='birthday')
    if emp_birthday:
        await callback.message.edit_text(text='\n'.join(emp_birthday.values()),
                                         reply_markup=create_inline_kb('back_to_movements_emp', 'cancel_all',
                                                                       width=1))
    else:
        await callback.message.edit_text(text=LEXICON_RU['select_employee']['not_birthdays'],
                                         reply_markup=create_inline_kb('back_to_movements_emp', 'cancel_all'))
    print(await state.get_state())
    print(await state.get_data())


# ____________________________________________________________


# !!!!!Испытательный срок заканчивается в ближайшее время!!!!!!!__________________________
# Показывает список сотрудников у которых ИС заканчивается в ближайшее время
@router.callback_query(StateFilter(FSMemploee.select_emp_category), Text(text=['duration_of_probation_finish_soon']))
async def category_by_cities(callback: CallbackQuery, state: FSMContext):
    emp_duration = get_information_by_categoryes(category='duration')
    if emp_duration:
        await callback.message.edit_text(text='\n'.join(emp_duration.values()),
                                     reply_markup=create_inline_kb('back_to_movements_emp', 'cancel_all',
                                                                   width=1))
    else:
        await callback.message.edit_text(text=LEXICON_RU['select_employee']['not_duration'],
                                         reply_markup=create_inline_kb('back_to_movements_emp', 'cancel_all'))

    print(await state.get_state())
    print(await state.get_data())
