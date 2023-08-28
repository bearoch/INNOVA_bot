'''В данном модуле располагаются модули, ответственные за команды основного меню'''

from aiogram import Router
from aiogram.filters import Command, StateFilter, Text
from aiogram.types import (Message, CallbackQuery)
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state

from lexicon.lexicon_ru import LEXICON_RU, TABLES, MOVEMENTS_EMP, MOVEMENTS_POS, SELECT_EMP, SELECT_EMP_CATEGORY, \
    SELECT_EMP_ON_DURATION, UPDATE_EMP, MOVEMENTS_SALARY
from keyboards.keyboards_utils import create_inline_kb
from states.states import FSMemploee, FSMpositions, FSMsalary

from bot import config

router: Router = Router()

#___________________________
# Срабатывает на команду старт, отправляет выбор таблиц
@router.message(Command(commands=['start']))
async def start_menu_button(message: Message, state: FSMContext):
    if message.text and message.from_user.id in config.tg_bot.admin_ids:
        await message.answer(text=LEXICON_RU['start'], reply_markup=create_inline_kb(width=1, **TABLES))
    else:
        await message.answer(text=LEXICON_RU['not_admin'])
        print(f'Незарегистрированный пользователь!!! ID: {message.from_user.id} - {message.from_user.full_name} @{message.from_user.username}')
    await state.clear()

# Возвращает в главное меню из любых модулей
@router.callback_query(Text(text=['back_to_start']))
@router.callback_query(Text(text=['cancel_all']), ~StateFilter(default_state))
async def start_return(callback: CallbackQuery, state: FSMContext):
    if callback.message.from_user.id in config.tg_bot.admin_ids:
        await callback.message.edit_text(text=LEXICON_RU['start'], reply_markup=create_inline_kb(width=1, **TABLES))
        await callback.answer(text='Главное меню')
    else:
        await callback.message.edit_text(text=LEXICON_RU['not_admin'])
        print(f'Незарегистрированный пользователь!!! ID: {callback.message.from_user.id} - {callback.message.from_user.full_name} @{callback.message.from_user.username}')
    await state.clear()


# Возвращает в главное меню из модулей export to excel
@router.callback_query(Text(text=['cancel_all_export']), ~StateFilter(default_state))
async def start_return_from_export(callback: CallbackQuery, state: FSMContext):
    if callback.message.from_user.id in config.tg_bot.admin_ids:
        await callback.message.answer(text=LEXICON_RU['start'], reply_markup=create_inline_kb(width=1, **TABLES))
        await callback.answer(text='Главное меню')
    else:
        await callback.message.answer(text=LEXICON_RU['not_admin'])
        print(f'Незарегистрированный пользователь!!! ID: {callback.message.from_user.id} - {callback.message.from_user.full_name} @{callback.message.from_user.username}')
    await state.clear()



#_______________________

# Выводит меню действий для таблицы сотрудники
@router.callback_query(Text(text=['employee']))
@router.callback_query(Text(text=['back_to_emp_actions']), ~StateFilter(default_state))
async def process_start_row(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text=LEXICON_RU['start_emp'], reply_markup=create_inline_kb(width=1, **MOVEMENTS_EMP))
    await callback.answer(text=LEXICON_RU['callback.answers']['go'])
    await state.set_state(FSMemploee.choose_action)

# SELECT
# Выводит меню действий для вывода информации из БД
@router.callback_query(Text(text=['select_emp']), StateFilter(FSMemploee.choose_action))
@router.callback_query(Text(text=['back_to_select_emp_actions']), ~StateFilter(default_state))
async def process_start_row(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text=LEXICON_RU['select_emp'], reply_markup=create_inline_kb(width=1, **SELECT_EMP))
    await callback.answer(text=LEXICON_RU['callback.answers']['go'])
    await state.set_state(FSMemploee.select_emp_actions)

# Выводит меню для вывода информации по категориям
@router.callback_query(Text(text=['category']), StateFilter(FSMemploee.select_emp_actions))
@router.callback_query(Text(text=['back_to_movements_emp']), ~StateFilter(default_state))
async def process_start_row(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text=LEXICON_RU['category'], reply_markup=create_inline_kb(width=1, **SELECT_EMP_CATEGORY))
    await callback.answer(text=LEXICON_RU['callback.answers']['go'])
    await state.set_state(FSMemploee.select_emp_category)

# Выводит меню для вывода информации по ИС
@router.callback_query(Text(text=['duration_of_probation_category']), StateFilter(FSMemploee.select_emp_category))
@router.callback_query(Text(text=['back_select_emp_on_duration_actions']), ~StateFilter(default_state))
async def process_start_row(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text=LEXICON_RU['category_duration'], reply_markup=create_inline_kb(width=1, **SELECT_EMP_ON_DURATION))
    await callback.answer(text=LEXICON_RU['callback.answers']['go'])
    await state.set_state(FSMemploee.select_emp_category)


# UPDATE
# Выводит варианты действий для изменения информации о сотруднике
@router.callback_query(Text(text=['update_emp']), StateFilter(FSMemploee.choose_action))
@router.callback_query(Text(text=['back_to_update_emp_actions']), ~StateFilter(default_state))
async def process_update_emp_actions(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text=LEXICON_RU['upd_del_row_employee']['upd_or_del'], reply_markup=create_inline_kb(width=1, **UPDATE_EMP))
    await callback.answer(text=LEXICON_RU['callback.answers']['go'])
    await state.set_state(FSMemploee.upd_dismissal_action)

#____________________________________








#______________________________________
# Выводит меню действий для таблицы истории должностей
@router.callback_query(Text(text=['positions']))
@router.callback_query(Text(text=['back_to_position_actions']), ~StateFilter(default_state))
async def process_start_row(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text=LEXICON_RU['start_emp'], reply_markup=create_inline_kb(width=1, **MOVEMENTS_POS))
    await callback.answer(text=LEXICON_RU['callback.answers']['go'])
    await state.set_state(FSMpositions.choose_action)


#______________________________________
# Выводит меню действий для таблицы истории зарплат сотрудников
@router.callback_query(Text(text=['salary']))
@router.callback_query(Text(text=['back_to_salary_actions']), ~StateFilter(default_state))
async def process_salary_actions(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text=LEXICON_RU['start_emp'], reply_markup=create_inline_kb(width=1, **MOVEMENTS_SALARY))
    await callback.answer(text=LEXICON_RU['callback.answers']['go'])
    await state.set_state(FSMsalary.choose_action)







# Этот хэндлер срабатывает на команду /help
@router.message(Command(commands=['help']), StateFilter(default_state))
async def process_help_command(message: Message):
    await message.answer(text=LEXICON_RU['/help'])


# Этот хэндлер будет срабатывать на команду "/cancel" в любых состояниях,
# кроме состояния по умолчанию, и отключать машину состояний
@router.message(Command(commands='cancel'), ~StateFilter(default_state))
async def process_cancel_command_state(message: Message, state: FSMContext):
    await message.answer(text=LEXICON_RU['cansel_if_yes'])
    # Сбрасываем состояние
    await state.clear()
    print(await state.get_state())
    print(await state.get_data())

# Этот хэндлер будет срабатывать на команду "/cancel" в состоянии
# по умолчанию и сообщать, что эта команда доступна в машине состояний
@router.message(Command(commands='cancel'), StateFilter(default_state))
async def process_cancel_command(message: Message):
    await message.answer(text=LEXICON_RU['cansel_if_no'])