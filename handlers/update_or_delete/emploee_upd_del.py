from aiogram.filters import StateFilter, Text
from aiogram.fsm.context import FSMContext
from aiogram import Router, F
from aiogram.fsm.state import default_state
from aiogram.types import (CallbackQuery, Message)

from models.methods.insert import InsertInto
from states.states import FSMemploee
from keyboards.keyboards_utils import create_inline_kb

from lexicon.lexicon_ru import LEXICON_RU
from filters.language_filter import CheckLenRowFilter, CheckUniqueFilter, CheckNameFilter, CheckDateFilter, \
    CheckIsdigitFilter
from models.methods.select import get_employee, information_about_employee, get_positions, get_duration, get_cityes, \
    get_list_employees
from models.methods.update import update_employee

router: Router = Router()


# запрашиваем фамилию или ID сотрудника
@router.callback_query(StateFilter(FSMemploee.upd_dismissal_action), Text(text=['update_employee_information']))
@router.callback_query(~StateFilter(default_state), Text(text=['upd_back_to_name_emp']))
async def process_start_upd(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text=LEXICON_RU['upd_del_row_employee']['name_employee'],
                                     reply_markup=create_inline_kb('back_to_update_emp_actions', 'cancel_all', width=1))

    await state.set_state(FSMemploee.upd_name_emp)
    await callback.answer(text=LEXICON_RU['callback.answers']['go'])
    print(await state.get_state())
    print(await state.get_data())


# _________________________________


# _________________________________
# получаем значение и ищем сотрудника, выводим найденные варианты
@router.message(StateFilter(FSMemploee.upd_name_emp))
async def process_upd_finding_emp(message: Message, state: FSMContext):
    if get_employee(message.text):
        await message.answer(text=LEXICON_RU['upd_del_row_employee']['choose_emp_from_list'],
                             reply_markup=create_inline_kb('upd_back_to_name_emp', 'cancel_all',
                                                           width=1, **get_employee(message.text)))

    else:
        await message.answer(text=LEXICON_RU['upd_del_row_employee']['repeat'],
                             reply_markup=create_inline_kb('cancel_all'))
    print(await state.get_state())
    print(await state.get_data())


# _________________________________


# _________________________________
# Выводим выбор текущих позиций из таблицы
@router.callback_query(StateFilter(FSMemploee.upd_name_emp))
@router.callback_query(~StateFilter(default_state), Text(text=['back_to_upd_actions']))
async def process_upd_actions(callback: CallbackQuery, state: FSMContext):
    if callback.data != 'back_to_upd_actions':
        await state.update_data(employee_id=callback.data)
    empl_information = information_about_employee(await state.get_data())
    if empl_information.get('upd_7_date_finish_duration', 0):
        del empl_information['upd_7_date_finish_duration']
    await callback.message.edit_text(text=LEXICON_RU['upd_del_row_employee']['actions'],
                                     reply_markup=create_inline_kb('upd_back_to_name_emp', 'cancel_all',
                                                                   width=1,
                                                                   **empl_information))
    await state.set_state(FSMemploee.set_new_meaning)
    print(await state.get_state())
    print(await state.get_data())


# _________________________________


# _________________________________
# Принимаем значение к изменению и направляем соответствующее сообщение, или клавиатуру с выбором
@router.callback_query(StateFilter(FSMemploee.set_new_meaning))
@router.callback_query(~StateFilter(default_state), Text(text=['back_to_changing_value']))
async def process_upd_move_to_form_for_update(callback: CallbackQuery, state: FSMContext):
    if callback.data != 'back_to_changing_value':
        await state.update_data(chose_value=callback.data)
    value = await state.get_data()
    if value['chose_value'] == 'upd_1_name':
        await callback.message.edit_text(text=LEXICON_RU['upd_del_row_employee']['upd_name_emp'],
                                         reply_markup=create_inline_kb('back_to_upd_actions', 'cancel_all'))
        await state.set_state(FSMemploee.upd_name_for_upd)

    elif value['chose_value'] == 'upd_2_position':
        await callback.message.edit_text(text=LEXICON_RU['upd_del_row_employee']['upd_position'],
                                         reply_markup=create_inline_kb('back_to_upd_actions',
                                                                       'cancel_all', **get_positions(
                                                 hold_pos=LEXICON_RU['add_row_emploee']['hold_positions'])))
        await state.set_state(FSMemploee.upd_position)

    elif value['chose_value'] == 'upd_3_date_empl':
        await callback.message.edit_text(text=LEXICON_RU['upd_del_row_employee']['upd_date_empl'],
                                         reply_markup=create_inline_kb('back_to_upd_actions', 'cancel_all'))
        await state.set_state(FSMemploee.upd_date_of_employment)

    elif value['chose_value'] == 'upd_4_salary_on_probation':
        await callback.message.edit_text(text=LEXICON_RU['upd_del_row_employee']['upd_salary_on_probation'],
                                         reply_markup=create_inline_kb('back_to_upd_actions', 'cancel_all'))
        await state.set_state(FSMemploee.upd_salary_on_probation)

    elif value['chose_value'] == 'upd_5_salary':
        await callback.message.edit_text(text=LEXICON_RU['upd_del_row_employee']['upd_salary'],
                                         reply_markup=create_inline_kb('back_to_upd_actions', 'cancel_all'))
        await state.set_state(FSMemploee.upd_salary)

    elif value['chose_value'] == 'upd_6_duration_of_probation':
        await callback.message.edit_text(text=LEXICON_RU['upd_del_row_employee']['upd_duration_of_probation'],
                                         reply_markup=create_inline_kb('add_new_duration', 'back_to_upd_actions',
                                                                       'cancel_all', **get_duration()))
        await state.set_state(FSMemploee.upd_duration_of_probation)

    elif value['chose_value'] == 'upd_8_city_of_residence':
        await callback.message.edit_text(text=LEXICON_RU['upd_del_row_employee']['upd_city_of_residence'],
                                         reply_markup=create_inline_kb('back_to_upd_actions',
                                                                       'cancel_all', **get_cityes('Казань')))
        await state.set_state(FSMemploee.upd_city_of_residence)

    elif value['chose_value'] == 'upd_9_phone_number':
        await callback.message.edit_text(text=LEXICON_RU['upd_del_row_employee']['upd_phone_number'],
                                         reply_markup=create_inline_kb('back_to_upd_actions', 'cancel_all'))
        await state.set_state(FSMemploee.upd_phone_number)

    elif value['chose_value'] == 'upd_99_date_of_birth':
        await callback.message.edit_text(text=LEXICON_RU['upd_del_row_employee']['upd_date_of_birth'],
                                         reply_markup=create_inline_kb('back_to_upd_actions', 'cancel_all'))
        await state.set_state(FSMemploee.upd_date_of_birth)


# _________________________________


# _________________________________
# Принимаем новое значение ФИО и отправляем подтверждение его записи в БД
@router.message(StateFilter(FSMemploee.upd_name_for_upd), CheckNameFilter(), CheckLenRowFilter(row_len=40),
                CheckUniqueFilter(table_values=get_list_employees()))
async def process_upd_name_emp(message: Message, state: FSMContext):
    await state.update_data(upd_new_name_emp=message.text)
    data = await state.get_data()
    await message.answer(text=f'Подтверждаете внесение изменения в ФИО сотрудника?\n'
                              f'Новое значение:\n'
                              f'{data["upd_new_name_emp"]}',
                         reply_markup=create_inline_kb('yes', 'no', 'back_to_changing_value', 'cancel_all'))
    await state.set_state(FSMemploee.upd_approve_new_name)


# Записывает новое ФИО в таблицу
@router.callback_query(StateFilter(FSMemploee.upd_approve_new_name))
async def process_upd_approve_new_name_emp(callback: CallbackQuery, state: FSMContext):
    if callback.data == 'yes':
        update_employee(column='name_employee', new_value=await state.get_data())
        await callback.answer(text=LEXICON_RU['callback.answers']['finish_yes'], show_alert=True)
    else:
        await callback.answer(text=LEXICON_RU['callback.answers']['finish_no'], show_alert=True)

    await callback.message.edit_text(text=LEXICON_RU['upd_del_row_employee']['actions'],
                                     reply_markup=create_inline_kb('upd_back_to_name_emp', 'cancel_all',
                                                                   width=1, **information_about_employee(
                                             await state.get_data())))
    await state.set_state(FSMemploee.set_new_meaning)
    print(await state.get_state())
    print(await state.get_data())


# _________________________________


# _________________________________
@router.message(StateFilter(FSMemploee.upd_position))
async def process_upd_finding_position(message: Message, state: FSMContext):
    if get_positions(name_pos=message.text):
        await message.answer(text=LEXICON_RU['upd_del_row_employee']['found_positions'],
                             reply_markup=create_inline_kb('back_to_changing_value', 'cancel_all',
                                                           width=1, **get_positions(name_pos=message.text)))
    else:
        await message.answer(text=LEXICON_RU['upd_del_row_employee']['repeat_pos'],
                             reply_markup=create_inline_kb('add_new_position', 'back_to_changing_value', 'cancel_all'))
    print(await state.get_state())
    print(await state.get_data())


# Принимаем новое значение должности и отправляем подтверждение его записи в БД
@router.callback_query(StateFilter(FSMemploee.upd_position))
async def process_upd_position_emp(callback: CallbackQuery, state: FSMContext):
    await state.update_data(position_id=callback.data)
    data = await state.get_data()
    await callback.message.edit_text(text=f'Подтверждаете изменение должности сотрудника?\n'
                                          f'Новое значение:\n'
                                          f'{get_positions(name_pos=data["position_id"])[data["position_id"]]}',
                                     reply_markup=create_inline_kb('yes', 'no', 'back_to_changing_value', 'cancel_all'))
    await state.set_state(FSMemploee.upd_approve_new_position)


# Записываем новую должность в таблицу
@router.callback_query(StateFilter(FSMemploee.upd_approve_new_position))
async def process_upd_approve_new_position(callback: CallbackQuery, state: FSMContext):
    if callback.data == 'yes':
        InsertInto.employee_position_row(await state.get_data())
        await callback.answer(text=LEXICON_RU['callback.answers']['finish_yes'], show_alert=True)
    else:
        await callback.answer(text=LEXICON_RU['callback.answers']['finish_no'], show_alert=True)

    await callback.message.edit_text(text=LEXICON_RU['upd_del_row_employee']['actions'],
                                     reply_markup=create_inline_kb('upd_back_to_name_emp', 'cancel_all',
                                                                   width=1, **{k: v for k, v in
                                                                               information_about_employee(
                                                                                   await state.get_data()).items() if
                                                                               k != 'upd_7_date_finish_duration'}))
    await state.set_state(FSMemploee.set_new_meaning)
    print(await state.get_state())
    print(await state.get_data())


# ___________________________________


# _________________________________
# Принимаем новое значение даты приема на работу и отправляем подтверждение его записи в БД
@router.message(StateFilter(FSMemploee.upd_date_of_employment), CheckDateFilter())
async def process_upd_date_of_employment(message: Message, state: FSMContext, new_date: str):
    await state.update_data(upd_new_date_of_employment=new_date)
    data = await state.get_data()
    await message.answer(text=f'Подтверждаете внесение изменения в дату приема сотрудника на работу?\n'
                              f'Новое значение:\n'
                              f'{message.text}',
                         reply_markup=create_inline_kb('yes', 'no', 'back_to_changing_value', 'cancel_all'))
    await state.set_state(FSMemploee.upd_approve_new_date_of_employment)


# Записывает новую дату устройства на работу в таблицу
@router.callback_query(StateFilter(FSMemploee.upd_approve_new_date_of_employment))
async def process_upd_approve_date_of_employment(callback: CallbackQuery, state: FSMContext):
    if callback.data == 'yes':
        update_employee(column='date_of_employment', new_value=await state.get_data())
        await callback.answer(text=LEXICON_RU['callback.answers']['finish_yes'], show_alert=True)
    else:
        await callback.answer(text=LEXICON_RU['callback.answers']['finish_no'], show_alert=True)

    await callback.message.edit_text(text=LEXICON_RU['upd_del_row_employee']['actions'],
                                     reply_markup=create_inline_kb('upd_back_to_name_emp', 'cancel_all',
                                                                   width=1, **{k: v for k, v in
                                                                               information_about_employee(
                                                                                   await state.get_data()).items() if
                                                                               k != 'upd_7_date_finish_duration'}))
    await state.set_state(FSMemploee.set_new_meaning)
    print(await state.get_state())
    print(await state.get_data())


# _________________________________


# _________________________________
# Принимаем новое значение зарплаты во время ИС и отправляем подтверждение ее записи в БД
@router.message(StateFilter(FSMemploee.upd_salary_on_probation), F.content_type == 'text',
                CheckIsdigitFilter(), CheckLenRowFilter(row_len=10))
async def process_upd_salary_on_probation(message: Message, state: FSMContext):
    await state.update_data(upd_new_salary_on_probation=message.text)
    data = await state.get_data()
    await message.answer(text=f'Подтверждаете внесение изменения в размер зарплаты сотрудника во время ИС\n'
                              f'Новое значение:\n'
                              f'{data["upd_new_salary_on_probation"]}',
                         reply_markup=create_inline_kb('yes', 'no', 'back_to_changing_value', 'cancel_all'))
    await state.set_state(FSMemploee.upd_approve_salary_on_probation)


# Записывает новую зарплату во время ИС в таблицу
@router.callback_query(StateFilter(FSMemploee.upd_approve_salary_on_probation))
async def process_upd_approve_new_salary_on_probation(callback: CallbackQuery, state: FSMContext):
    if callback.data == 'yes':
        update_employee(column='salary_on_probation', new_value=await state.get_data())
        await callback.answer(text=LEXICON_RU['callback.answers']['finish_yes'], show_alert=True)
    else:
        await callback.answer(text=LEXICON_RU['callback.answers']['finish_no'], show_alert=True)

    await callback.message.edit_text(text=LEXICON_RU['upd_del_row_employee']['actions'],
                                     reply_markup=create_inline_kb('upd_back_to_name_emp', 'cancel_all',
                                                                   width=1, **{k: v for k, v in
                                                                               information_about_employee(
                                                                                   await state.get_data()).items() if
                                                                               k != 'upd_7_date_finish_duration'}))
    await state.set_state(FSMemploee.set_new_meaning)
    print(await state.get_state())
    print(await state.get_data())


# _________________________________


# _________________________________
# Принимаем новое значение зарплаты и отправляем подтверждение ее записи в БД в таблицу истории зарплат
@router.message(StateFilter(FSMemploee.upd_salary), F.content_type == 'text',
                CheckIsdigitFilter(), CheckLenRowFilter(row_len=10))
async def process_upd_salary(message: Message, state: FSMContext):
    await state.update_data(salary=message.text)
    data = await state.get_data()
    await message.answer(text=f'Подтверждаете внесение изменения в размер зарплаты сотрудника\n'
                              f'Новое значение:\n'
                              f'{data["salary"]}',
                         reply_markup=create_inline_kb('yes', 'no', 'back_to_changing_value', 'cancel_all'))
    await state.set_state(FSMemploee.upd_approve_salary)


# Записывает новую зарплату во время ИС в таблицу
@router.callback_query(StateFilter(FSMemploee.upd_approve_salary))
async def process_upd_approve_new_salary(callback: CallbackQuery, state: FSMContext):
    if callback.data == 'yes':
        InsertInto.salary_history_row(await state.get_data())
        await callback.answer(text=LEXICON_RU['callback.answers']['finish_yes'], show_alert=True)
    else:
        await callback.answer(text=LEXICON_RU['callback.answers']['finish_no'], show_alert=True)

    await callback.message.edit_text(text=LEXICON_RU['upd_del_row_employee']['actions'],
                                     reply_markup=create_inline_kb('upd_back_to_name_emp', 'cancel_all',
                                                                   width=1, **{k: v for k, v in
                                                                               information_about_employee(
                                                                                   await state.get_data()).items() if
                                                                               k != 'upd_7_date_finish_duration'}))
    await state.set_state(FSMemploee.set_new_meaning)
    print(await state.get_state())
    print(await state.get_data())


# _________________________________


# _________________________________
# Принимаем новое значение продолжительности ИС и отправляем подтверждение его записи в БД
@router.callback_query(StateFilter(FSMemploee.upd_duration_of_probation))
async def process_upd_duration_of_probation(callback: CallbackQuery, state: FSMContext):
    await state.update_data(upd_duration_of_probation=callback.data)
    data = await state.get_data()
    await callback.message.edit_text(text=f'Подтверждаете изменение продолжительности ИС сотрудника?\n'
                                          f'Новое значение:\n'
                                          f'{get_duration()[data["upd_duration_of_probation"]]}',
                                     reply_markup=create_inline_kb('yes', 'no', 'back_to_changing_value', 'cancel_all'))
    await state.set_state(FSMemploee.upd_approve_new_duration_of_probation)


# Записываем новую продолжительность ИС в таблицу
@router.callback_query(StateFilter(FSMemploee.upd_approve_new_duration_of_probation))
async def process_upd_approve_new_duration_of_probation(callback: CallbackQuery, state: FSMContext):
    if callback.data == 'yes':
        update_employee(column='duration_of_probation_id', new_value=await state.get_data())
        await callback.answer(text=LEXICON_RU['callback.answers']['finish_yes'], show_alert=True)
    else:
        await callback.answer(text=LEXICON_RU['callback.answers']['finish_no'], show_alert=True)

    await callback.message.edit_text(text=LEXICON_RU['upd_del_row_employee']['actions'],
                                     reply_markup=create_inline_kb('upd_back_to_name_emp', 'cancel_all',
                                                                   width=1, **{k: v for k, v in
                                                                               information_about_employee(
                                                                                   await state.get_data()).items() if
                                                                               k != 'upd_7_date_finish_duration'}))
    await state.set_state(FSMemploee.set_new_meaning)
    print(await state.get_state())
    print(await state.get_data())


# ___________________________________


# _________________________________
# После ввода начала названия города выводим варианты для выбора
@router.message(StateFilter(FSMemploee.upd_city_of_residence))
async def process_upd_finding_city(message: Message, state: FSMContext):
    if get_cityes(message.text):
        await message.answer(text=LEXICON_RU['upd_del_row_employee']['found_cities'],
                             reply_markup=create_inline_kb('back_to_changing_value', 'cancel_all',
                                                           width=1, **get_cityes(message.text)))
    else:
        await message.answer(text=LEXICON_RU['upd_del_row_employee']['repeat_city'],
                             reply_markup=create_inline_kb('add_new_city', 'back_to_changing_value', 'cancel_all'))
    print(await state.get_state())
    print(await state.get_data())


# Принимаем новое значение города проживания и отправляем подтверждение его записи в БД
@router.callback_query(StateFilter(FSMemploee.upd_city_of_residence))
async def process_upd_city_of_residence(callback: CallbackQuery, state: FSMContext):
    await state.update_data(upd_city_of_residence=callback.data)
    data = await state.get_data()
    await callback.message.edit_text(text=f'Подтверждаете изменение города проживания сотрудника?\n'
                                          f'Новое значение:\n'
                                          f'{get_cityes()[data["upd_city_of_residence"]]}',
                                     reply_markup=create_inline_kb('yes', 'no', 'back_to_changing_value', 'cancel_all'))
    await state.set_state(FSMemploee.upd_approve_new_city_of_residence)


# Записываем новый город проживания в таблицу
@router.callback_query(StateFilter(FSMemploee.upd_approve_new_city_of_residence))
async def process_upd_approve_new_city_of_residence(callback: CallbackQuery, state: FSMContext):
    if callback.data == 'yes':
        update_employee(column='city_of_residence_id', new_value=await state.get_data())
        await callback.answer(text=LEXICON_RU['callback.answers']['finish_yes'], show_alert=True)
    else:
        await callback.answer(text=LEXICON_RU['callback.answers']['finish_no'], show_alert=True)

    await callback.message.edit_text(text=LEXICON_RU['upd_del_row_employee']['actions'],
                                     reply_markup=create_inline_kb('upd_back_to_name_emp', 'cancel_all',
                                                                   width=1, **{k: v for k, v in
                                                                               information_about_employee(
                                                                                   await state.get_data()).items() if
                                                                               k != 'upd_7_date_finish_duration'}))
    await state.set_state(FSMemploee.set_new_meaning)
    print(await state.get_state())
    print(await state.get_data())


# ___________________________________


# _________________________________
# Принимаем новое значение телефонного номера и отправляем подтверждение его записи в БД
@router.message(StateFilter(FSMemploee.upd_phone_number), F.content_type == 'text', CheckIsdigitFilter(),
                CheckLenRowFilter(row_len=10))
async def process_upd_phone_number(message: Message, state: FSMContext):
    await state.update_data(upd_new_phone_number=message.text)
    data = await state.get_data()
    await message.answer(text=f'Подтверждаете новый телефонный номер сотрудника?\n'
                              f'Новое значение:\n'
                              f'{data["upd_new_phone_number"]}',
                         reply_markup=create_inline_kb('yes', 'no', 'back_to_changing_value', 'cancel_all'))
    await state.set_state(FSMemploee.upd_approve_new_phone_number)


# Записывает новый телефонный номер в таблицу
@router.callback_query(StateFilter(FSMemploee.upd_approve_new_phone_number))
async def process_upd_approve_new_salary_on_probation(callback: CallbackQuery, state: FSMContext):
    if callback.data == 'yes':
        update_employee(column='phone_number', new_value=await state.get_data())
        await callback.answer(text=LEXICON_RU['callback.answers']['finish_yes'], show_alert=True)
    else:
        await callback.answer(text=LEXICON_RU['callback.answers']['finish_no'], show_alert=True)

    await callback.message.edit_text(text=LEXICON_RU['upd_del_row_employee']['actions'],
                                     reply_markup=create_inline_kb('upd_back_to_name_emp', 'cancel_all',
                                                                   width=1, **{k: v for k, v in
                                                                               information_about_employee(
                                                                                   await state.get_data()).items() if
                                                                               k != 'upd_7_date_finish_duration'}))
    await state.set_state(FSMemploee.set_new_meaning)
    print(await state.get_state())
    print(await state.get_data())


# _________________________________


# _________________________________
# Принимаем новое значение даты рождения и отправляем подтверждение его записи в БД
@router.message(StateFilter(FSMemploee.upd_date_of_birth), CheckDateFilter())
async def process_upd_date_of_birth(message: Message, state: FSMContext, new_date: str):
    await state.update_data(upd_new_date_of_birth=new_date)
    data = await state.get_data()
    await message.answer(text=f'Подтверждаете внесение изменения в дату рождения сотрудника?\n'
                              f'Новое значение:\n'
                              f'{message.text}',
                         reply_markup=create_inline_kb('yes', 'no', 'back_to_changing_value', 'cancel_all'))
    await state.set_state(FSMemploee.upd_approve_new_date_of_birth)


# Записывает новую дату устройства на работу в таблицу
@router.callback_query(StateFilter(FSMemploee.upd_approve_new_date_of_birth))
async def process_upd_approve_date_of_employment(callback: CallbackQuery, state: FSMContext):
    if callback.data == 'yes':
        update_employee(column='date_of_birth', new_value=await state.get_data())
        await callback.answer(text=LEXICON_RU['callback.answers']['finish_yes'], show_alert=True)
    else:
        await callback.answer(text=LEXICON_RU['callback.answers']['finish_no'], show_alert=True)

    await callback.message.edit_text(text=LEXICON_RU['upd_del_row_employee']['actions'],
                                     reply_markup=create_inline_kb('upd_back_to_name_emp', 'cancel_all',
                                                                   width=1, **{k: v for k, v in
                                                                               information_about_employee(
                                                                                   await state.get_data()).items() if
                                                                               k != 'upd_7_date_finish_duration'}))
    await state.set_state(FSMemploee.set_new_meaning)
    print(await state.get_state())
    print(await state.get_data())
# _________________________________
