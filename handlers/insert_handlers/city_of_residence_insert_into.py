from aiogram.filters import StateFilter, Text
from aiogram.fsm.context import FSMContext
from aiogram import Router, F
from aiogram.types import (CallbackQuery, Message)
from states.states import FSMemploee
from keyboards.keyboards_utils import create_inline_kb_arg, create_inline_kb
from models.methods.insert import InsertInto
from lexicon.lexicon_ru import LEXICON_RU
from filters.language_filter import CheckCityFilter, CheckLenRowFilter, CheckUniqueFilter
from models.methods.select import get_cityes

router: Router = Router()


@router.callback_query(StateFilter(FSMemploee.city_of_residence_id), Text(text=['add_new_city']))
@router.callback_query(StateFilter(FSMemploee.upd_city_of_residence), Text(text=['add_new_city']))
async def process_add_new_duration_of_prob(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    if data.get('chose_value', 0) == 0:
        await callback.message.edit_text(text=LEXICON_RU['add_row_emploee']['name_city'],
                                         reply_markup=create_inline_kb('back_to_city', 'cancel_all'))
    else:
        await callback.message.edit_text(text=LEXICON_RU['add_row_emploee']['name_city'],
                                         reply_markup=create_inline_kb('back_to_changing_value', 'cancel_all'))
    await state.set_state(FSMemploee.name_city)
    await callback.answer(text=LEXICON_RU['callback.answers']['go'])
    print(await state.get_state())
    print(await state.get_data())



@router.message(StateFilter(FSMemploee.name_city), F.content_type == 'text', CheckCityFilter(),
                CheckLenRowFilter(row_len=40), CheckUniqueFilter(table_values=get_cityes()))
#@router.message(StateFilter(FSMemploee.upd_city_of_residence), F.content_type == 'text', CheckCityFilter(),
#                CheckLenRowFilter(row_len=40), CheckUniqueFilter(table_values=get_cityes()))
async def process_add_new_city(message: Message, state: FSMContext):
    await state.update_data(name_city=message.text)
    data = await state.get_data()
    await message.answer(text=f'Подтвердите указанную ранее информацию:\n'
                              f'Название города: {data["name_city"]}',
                         reply_markup=create_inline_kb('yes', 'no', width=1))
    await state.set_state(FSMemploee.approve_city)
    print(await state.get_state())
    print(await state.get_data())


@router.callback_query(StateFilter(FSMemploee.approve_city))
async def process_add_approve(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()

    if callback.data == 'yes':
        InsertInto.city_of_residence_row(await state.get_data())
        await callback.answer(text=LEXICON_RU['callback.answers']['finish_yes'], show_alert=True)
    else:
        await callback.answer(text=LEXICON_RU['callback.answers']['finish_no'], show_alert=True)

    if data.get('chose_value', 0) == 0:
        if data['answer_probation'] == 'Нет':
            await callback.message.edit_text(text=LEXICON_RU['add_row_emploee']['city_of_residence_id'],
                                             reply_markup=create_inline_kb('back_to_salary_without_probation',
                                                                           'cancel_all', width=1,
                                                                           **get_cityes('Казань')))
        elif data['answer_probation'] == 'Да':
            await callback.message.edit_text(text=LEXICON_RU['add_row_emploee']['city_of_residence_id'],
                                             reply_markup=create_inline_kb('back_to_salary_with_probation',
                                                                           'cancel_all', width=1,
                                                                           **get_cityes('Казань')))
        await state.set_state(FSMemploee.city_of_residence_id)

    else:
        await callback.message.edit_text(text=LEXICON_RU['upd_del_row_employee']['upd_city_of_residence'],
                                         reply_markup=create_inline_kb('back_to_upd_actions',
                                                                       'cancel_all', **get_cityes('Казань')))
        await state.set_state(FSMemploee.upd_city_of_residence)
    print(await state.get_state())
    print(await state.get_data())
