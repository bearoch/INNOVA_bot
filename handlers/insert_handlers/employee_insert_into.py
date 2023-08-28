from datetime import datetime

from aiogram import F
from aiogram.filters import StateFilter, Text
from aiogram.fsm.context import FSMContext
from aiogram import Router
from aiogram.fsm.state import default_state
from aiogram.types import (CallbackQuery, Message)
from states.states import FSMemploee
from keyboards.keyboards_utils import create_inline_kb, create_inline_kb_arg
from models.methods.select import get_positions, get_duration, get_cityes, get_list_employees
from models.methods.insert import InsertInto
from lexicon.lexicon_ru import LEXICON_RU, TABLES
from filters.language_filter import CheckIsdigitFilter, CheckNameFilter, CheckDateFilter, CheckLenRowFilter, \
    CheckUniqueFilter

router: Router = Router()


# router.message.filter(StateFilter(FSMmain.fill_add_row))

# Строка для ввода ФИО нового сотрудника
@router.callback_query(Text(text=['add_employee']), StateFilter(FSMemploee.choose_action))
@router.callback_query(Text(text=['back_to_name_emp']), StateFilter(FSMemploee.position_id))
async def process_start_row(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text=LEXICON_RU['add_row_emploee']['name'],
                                     reply_markup=create_inline_kb('back_to_emp_actions', 'cancel_all'))
    await state.set_state(FSMemploee.name_employee)
    print(await state.get_state())
    await callback.answer(text=LEXICON_RU['callback.answers']['go'])


# ______________________________
# Запись имени нового сотрудника и выбор должности, или создание новой должности
@router.message(StateFilter(FSMemploee.name_employee), F.content_type == 'text', CheckNameFilter(),
                CheckLenRowFilter(row_len=40), CheckUniqueFilter(table_values=get_list_employees()))
async def process_add_position(message: Message, state: FSMContext, new_name: str):
    await state.update_data(name_employee=new_name)
    await message.answer(text=LEXICON_RU['add_row_emploee']['add_position'],
                         reply_markup=create_inline_kb('back_to_name_emp', 'cancel_all', width=1,
                                                       **get_positions(hold_pos=LEXICON_RU['add_row_emploee']['hold_positions'])))
    await state.set_state(FSMemploee.position_id)
    print(await state.get_state())
    print(await state.get_data())


# Отработка кнопки назад со следующего шага
@router.callback_query(StateFilter(FSMemploee.date_of_employment), Text(text=['back_to_choose_position']))
@router.callback_query(StateFilter(FSMemploee.name_position), Text(text=['back_to_choose_position']))
@router.callback_query(StateFilter(FSMemploee.position_id), Text(text=['searcher_position']))
async def back_to_position(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text=LEXICON_RU['add_row_emploee']['add_position'],
                                     reply_markup=create_inline_kb('back_to_name_emp', 'cancel_all',
                                                                   width=1,
                                                                   **get_positions(hold_pos=LEXICON_RU['add_row_emploee']['hold_positions'])))
    await state.set_state(FSMemploee.position_id)
    print(await state.get_state())
    print(await state.get_data())


# После ввода начала названия должности выводим варианты для выбора
@router.message(StateFilter(FSMemploee.position_id))
async def process_finding_position(message: Message, state: FSMContext):
    if get_positions(name_pos=message.text):
        await message.answer(text=LEXICON_RU['add_row_emploee']['found_positions'],
                             reply_markup=create_inline_kb('searcher_position', 'cancel_all',
                                                           width=1, **get_positions(name_pos=message.text)))
    else:
        await message.answer(text=LEXICON_RU['add_row_emploee']['repeat_pos'],
                             reply_markup=create_inline_kb('add_new_position', 'searcher_position', 'cancel_all'))
    print(await state.get_state())
    print(await state.get_data())
# _______________________________





# ______________________________
# Запись позиции и предложение ввести дату найма сотрудника
@router.callback_query(StateFilter(FSMemploee.position_id))
@router.callback_query(StateFilter(FSMemploee.have_probation_or_not), Text(text=['back_to_date_employment']))
async def process_add_date_employment(callback: CallbackQuery, state: FSMContext):
    if not callback.data == 'back_to_date_employment':
        await state.update_data(position_id=callback.data)
    await callback.message.edit_text(text=LEXICON_RU['add_row_emploee']['date_of_employment'],
                                     reply_markup=create_inline_kb('back_to_choose_position', 'cancel_all'))
    await state.set_state(FSMemploee.date_of_employment)
    await callback.answer(text=LEXICON_RU['callback.answers']['success'])
    print(await state.get_state())
    print(await state.get_data())


# _______________________________
# Запись даты приема на работу и запрос на наличие испытательного срока
@router.message(StateFilter(FSMemploee.date_of_employment), F.content_type == 'text', CheckDateFilter())
async def process_have_probation_or_not(message: Message, state: FSMContext, new_date: str):
    await state.update_data(date_of_employment=new_date)
    await message.answer(text=LEXICON_RU['add_row_emploee']['have_probation_or_not'],
                         reply_markup=create_inline_kb('yes', 'no', 'back_to_date_employment', 'cancel_all'))
    await state.set_state(FSMemploee.have_probation_or_not)
    print(await state.get_state())
    print(await state.get_data())

# Отработка кнопки назад со следующего шага
@router.callback_query(StateFilter(FSMemploee.salary), Text(text=['back_to_have_probation_or_not']))
@router.callback_query(StateFilter(FSMemploee.duration_of_probation_id), Text(text=['back_to_have_probation_or_not']))
async def back_to_have_probation_or_not(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text=LEXICON_RU['add_row_emploee']['have_probation_or_not'],
                                     reply_markup=create_inline_kb('yes', 'no', 'back_to_date_employment',
                                                                   'cancel_all'))
    await state.set_state(FSMemploee.have_probation_or_not)
    print(await state.get_state())
    print(await state.get_data())
# ___________________________________



# ____________________________________
# Принимает ответ о наличии испытательного срока и переводит на соответствующий шаг
@router.callback_query(StateFilter(FSMemploee.have_probation_or_not))
@router.callback_query(StateFilter(FSMemploee.salary_on_probation), Text(text=['back_to_duration_of_prob']))
@router.callback_query(StateFilter(FSMemploee.new_duration), Text(text=['back_to_duration_of_prob']))
@router.callback_query(StateFilter(FSMemploee.city_of_residence_id), Text(text=['back_to_salary_without_probation']))
async def back_to_have_probation_or_not_answer(callback: CallbackQuery, state: FSMContext):
    if callback.data in ['yes', 'no']:
        if callback.data == 'yes':
            await state.update_data(answer_probation='Да')
        else:
            await state.update_data(answer_probation='Нет')
    data = await state.get_data()
    if data['answer_probation'] == 'Да':
        await callback.message.edit_text(text=LEXICON_RU['add_row_emploee']['duration_of_probation_id'],
                                         reply_markup=create_inline_kb('add_new_duration',
                                                                       'back_to_have_probation_or_not',
                                                                       'cancel_all', width=1, **get_duration()))
        await state.set_state(FSMemploee.duration_of_probation_id)

    elif data['answer_probation'] == 'Нет':
        await callback.message.edit_text(text=LEXICON_RU['add_row_emploee']['salary_without_probation'],
                                         reply_markup=create_inline_kb('back_to_have_probation_or_not', 'cancel_all'))
        await state.set_state(FSMemploee.salary)

    print(await state.get_state())
    print(await state.get_data())
#_________________________________



# _________________________________
# Принимает и записывает ID ИС и предлагает ввести объем зарплаты сотрудника во время ИС
@router.callback_query(StateFilter(FSMemploee.duration_of_probation_id))
@router.callback_query(StateFilter(FSMemploee.salary), Text(text=['back_to_salary_on_pron']))
async def process_add_salary_on_probation(callback: CallbackQuery, state: FSMContext):
    if not callback.data == 'back_to_salary_on_pron':
        await state.update_data(duration_of_probation_id=callback.data)
    await callback.message.edit_text(text=LEXICON_RU['add_row_emploee']['salary_on_probation'],
                                     reply_markup=create_inline_kb('back_to_duration_of_prob', 'cancel_all'))
    await state.set_state(FSMemploee.salary_on_probation)
    await callback.answer(text=LEXICON_RU['callback.answers']['success'])
    print(await state.get_state())
    print(await state.get_data())
#____________________________________



#____________________________________
# Запись зарплаты во время испытательного срока и предложение ввести объем зарплаты после ИС
@router.message(StateFilter(FSMemploee.salary_on_probation), F.content_type == 'text', CheckIsdigitFilter(),
                CheckLenRowFilter(row_len=10))
async def process_add_salary_after_probation(message: Message, state: FSMContext):
    await state.update_data(salary_on_probation=message.text)
    await message.answer(text=LEXICON_RU['add_row_emploee']['salary'],
                         reply_markup=create_inline_kb('back_to_salary_on_pron', 'cancel_all'))
    await state.set_state(FSMemploee.salary)
    print(await state.get_state())
    print(await state.get_data())

# Отработка кнопки назад со следующего шага
@router.callback_query(StateFilter(FSMemploee.city_of_residence_id), Text(text=['back_to_salary_with_probation']))
async def process_back_to_salary_after_probation(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text=LEXICON_RU['add_row_emploee']['salary'],
                                     reply_markup=create_inline_kb('back_to_salary_on_pron', 'cancel_all'))
    await state.set_state(FSMemploee.salary)
    print(await state.get_state())
    print(await state.get_data())
#__________________________________




# ________________________________
# Записывает объем зарплаты, предлагает выбрать город проживания сотрудника
@router.message(StateFilter(FSMemploee.salary), CheckIsdigitFilter(), CheckLenRowFilter(row_len=10))
async def process_add_city_of_residence(message: Message, state: FSMContext):
    data = await state.get_data()
    await state.update_data(salary=message.text)
    if data['answer_probation'] == 'Нет':
        await message.answer(text=LEXICON_RU['add_row_emploee']['city_of_residence_id'],
                             reply_markup=create_inline_kb('back_to_salary_without_probation',
                                                           'cancel_all', width=1, **get_cityes('Казань')))
    elif data['answer_probation'] == 'Да':
        await message.answer(text=LEXICON_RU['add_row_emploee']['city_of_residence_id'],
                             reply_markup=create_inline_kb('back_to_salary_with_probation',
                                                           'cancel_all', width=1, **get_cityes('Казань')))
    await state.set_state(FSMemploee.city_of_residence_id)
    print(await state.get_state())
    print(await state.get_data())


# Отработка кнопки назад со следующего шага
@router.callback_query(StateFilter(FSMemploee.city_of_residence_id), Text(text=['searcher_city']))
@router.callback_query(StateFilter(FSMemploee.phone_number), Text(text=['back_to_city']))
@router.callback_query(StateFilter(FSMemploee.name_city), Text(text=['back_to_city']))
async def back_to_city(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    if data['answer_probation'] == 'Нет':
        await callback.message.edit_text(text=LEXICON_RU['add_row_emploee']['city_of_residence_id'],
                                         reply_markup=create_inline_kb('back_to_salary_without_probation',
                                                                       'cancel_all', width=1, **get_cityes('Казань')))
    elif data['answer_probation'] == 'Да':
        await callback.message.edit_text(text=LEXICON_RU['add_row_emploee']['city_of_residence_id'],
                                         reply_markup=create_inline_kb('back_to_salary_with_probation',
                                                                       'cancel_all', width=1, **get_cityes('Казань')))
    await state.set_state(FSMemploee.city_of_residence_id)
    print(await state.get_state())
    print(await state.get_data())


# После ввода начала названия города выводим варианты для выбора
@router.message(StateFilter(FSMemploee.city_of_residence_id))
async def process_upd_finding_emp(message: Message, state: FSMContext):
    if get_cityes(message.text):
        await message.answer(text=LEXICON_RU['add_row_emploee']['found_cities'],
                             reply_markup=create_inline_kb('searcher_city', 'cancel_all',
                                                           width=1, **get_cityes(message.text)))
    else:
        await message.answer(text=LEXICON_RU['add_row_emploee']['repeat'],
                             reply_markup=create_inline_kb('add_new_city', 'searcher_city', 'cancel_all'))
    print(await state.get_state())
    print(await state.get_data())
#___________________________________



# _________________________________
# Записывает ID города проживания сотрудника, предлагает ввести телефонный номер
@router.callback_query(StateFilter(FSMemploee.city_of_residence_id))
@router.callback_query(StateFilter(FSMemploee.date_of_birth), Text(text=['back_to_phone']))
async def process_add_phone_number(callback: CallbackQuery, state: FSMContext):
    if not callback.data == 'back_to_phone':
        await state.update_data(city_of_residence_id=callback.data)
    await callback.message.edit_text(text=LEXICON_RU['add_row_emploee']['phone_number'],
                                     reply_markup=create_inline_kb('back_to_city', 'cancel_all'))
    await state.set_state(FSMemploee.phone_number)
    await callback.answer(text=LEXICON_RU['callback.answers']['success'])
    print(await state.get_state())
    print(await state.get_data())
# __________________________________



# ___________________________________
# Записывает номер телефона сотрудника, предлагает ввести дату рождения
@router.message(StateFilter(FSMemploee.phone_number), F.content_type == 'text', CheckIsdigitFilter(),
                CheckLenRowFilter(row_len=10))
async def process_add_date_of_birth(message: Message, state: FSMContext):
    await state.update_data(phone_number=message.text)
    await message.answer(text=LEXICON_RU['add_row_emploee']['date_of_birth'],
                         reply_markup=create_inline_kb('back_to_phone', 'cancel_all'))
    await state.set_state(FSMemploee.date_of_birth)
    print(await state.get_state())
    print(await state.get_data())


# Отработка кнопки назад со следующего шага
@router.callback_query(StateFilter(FSMemploee.approve), Text(text=['back_to_date_of_birth']))
async def back_to_date_of_birth(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text=LEXICON_RU['add_row_emploee']['date_of_birth'],
                                     reply_markup=create_inline_kb('back_to_phone', 'cancel_all'))
    await state.set_state(FSMemploee.date_of_birth)
    print(await state.get_state())
    print(await state.get_data())
# ____________________________


# ______________________________
@router.message(StateFilter(FSMemploee.date_of_birth), F.content_type == 'text', CheckDateFilter())
async def process_add_approve_information(message: Message, state: FSMContext, new_date: str):
    await state.update_data(date_of_birth=new_date)

    all_row = await state.get_data()
    if all_row['answer_probation'] == 'Да':
        await message.answer(text=f'Подтвердите указанную ранее информацию:\n'
                                  f'ФИО - {all_row["name_employee"]}\n'
                                  f'Должность - {get_positions(name_pos=all_row["position_id"])[all_row["position_id"]]}\n'
                                  f'Дата приема на работу - {datetime.strptime(all_row["date_of_employment"], "%Y.%m.%d").strftime("%d.%m.%Y")}\n'
                                  f'ЗП во время ИС - {all_row["salary_on_probation"]} руб.\n'
                                  f'Длительность ИС - {get_duration()[all_row["duration_of_probation_id"]]} дней\n'
                                  f'Зарплата после ИС - {all_row["salary"]} руб.\n'
                                  f'Город проживания - {get_cityes()[all_row["city_of_residence_id"]]}\n'
                                  f'Телефонный номер - ({all_row["phone_number"][0:3]}) {all_row["phone_number"][3:6]}-'
                                  f'{all_row["phone_number"][6:8]}-{all_row["phone_number"][8:10]}\n'
                                  f'Дата рождения - {datetime.strptime(all_row["date_of_birth"], "%Y.%m.%d").strftime("%d.%m.%Y")}',

                             reply_markup=create_inline_kb('yes', 'no', 'back_to_date_of_birth', 'cancel_all', width=1))
    elif all_row['answer_probation'] == 'Нет':
        await message.answer(text=f'Подтвердите указанную ранее информацию:\n'
                                  f'ФИО - {all_row["name_employee"]}\n'
                                  f'Должность - {get_positions(name_pos=all_row["position_id"])[all_row["position_id"]]}\n'
                                  f'Дата приема на работу - {datetime.strptime(all_row["date_of_employment"], "%Y.%m.%d").strftime("%d.%m.%Y")}\n'
                                  f'Заработная плата - {all_row["salary"]} руб.\n'
                                  f'Город проживания - {get_cityes()[all_row["city_of_residence_id"]]}\n'
                                  f'Телефонный номер - ({all_row["phone_number"][0:3]}) {all_row["phone_number"][3:6]}-'
                                  f'{all_row["phone_number"][6:8]}-{all_row["phone_number"][8:10]}\n'
                                  f'Дата рождения - {datetime.strptime(all_row["date_of_birth"], "%Y.%m.%d").strftime("%d.%m.%Y")}',

                             reply_markup=create_inline_kb('yes', 'no', 'back_to_date_of_birth', 'cancel_all', width=1))


    await state.set_state(FSMemploee.approve)
    print(await state.get_state())
    print(await state.get_data())


@router.callback_query(StateFilter(FSMemploee.approve))
async def process_add_row_in_employee_tab(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    if callback.data == 'yes':
        InsertInto.employee_insert_row(await state.get_data())
        InsertInto.salary_history_row(await state.get_data())
        InsertInto.employee_position_row(await state.get_data())
        await callback.message.answer(text=LEXICON_RU['add_row_emploee']['finish_yes'])
        await callback.answer(text=LEXICON_RU['callback.answers']['finish_yes'], show_alert=True)
    else:
        await callback.message.answer(text=LEXICON_RU['add_row_emploee']['finish_no'])
        await callback.answer(text=LEXICON_RU['callback.answers']['finish_no'], show_alert=True)

    await callback.message.answer(text=LEXICON_RU['start'], reply_markup=create_inline_kb(width=1, **TABLES))
    await state.clear()
