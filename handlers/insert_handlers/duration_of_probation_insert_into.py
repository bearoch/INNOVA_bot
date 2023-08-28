from aiogram.filters import StateFilter, Text
from aiogram.fsm.context import FSMContext
from aiogram import Router, F
from aiogram.types import (CallbackQuery, Message)
from states.states import FSMemploee
from keyboards.keyboards_utils import create_inline_kb_arg, create_inline_kb
from models.methods.insert import InsertInto
from lexicon.lexicon_ru import LEXICON_RU
from filters.language_filter import CheckIsdigitFilter, CheckUniqueFilter
from models.methods.select import get_duration

router: Router = Router()


# Добавление нового значения испытательного срока в таблицу испытательных сроков
@router.callback_query(StateFilter(FSMemploee.duration_of_probation_id), Text(text=['add_new_duration']))
@router.callback_query(StateFilter(FSMemploee.upd_duration_of_probation), Text(text=['add_new_duration']))
async def process_add_new_duration_of_prob(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text=LEXICON_RU['add_row_emploee']['add_duration'],
                                     reply_markup=create_inline_kb('back_to_duration_of_prob'))
    await state.set_state(FSMemploee.new_duration)
    await callback.answer(text=LEXICON_RU['callback.answers']['go'])
    print(await state.get_state())
    print(await state.get_data())


# Принимает значение объема испытательного срока
@router.message(StateFilter(FSMemploee.new_duration), F.content_type == 'text', CheckIsdigitFilter(),
                CheckUniqueFilter(table_values=get_duration()))
async def process_add_new_duration(message: Message, state: FSMContext):
    await state.update_data(new_duration=message.text)
    data = await state.get_data()
    await message.answer(text=f'Подтвердите указанную ранее информацию:\n'
                              f'Длительность испытательного срока: {data["new_duration"]}',
                         reply_markup=create_inline_kb('yes', 'no', width=1))
    await state.set_state(FSMemploee.approve_duration)
    print(await state.get_state())
    print(await state.get_data())


# Принимает подтверждение и записывает новое значение
@router.callback_query(StateFilter(FSMemploee.approve_duration))
async def process_add_approve(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    if callback.data == 'yes':
        InsertInto.duration_of_probation_row(await state.get_data())
        await callback.answer(text=LEXICON_RU['callback.answers']['finish_yes'], show_alert=True)
    else:
        await callback.answer(text=LEXICON_RU['callback.answers']['finish_no'], show_alert=True)

    if data.get('answer_probation', 0) == 'Да':
        await callback.message.edit_text(text=LEXICON_RU['add_row_emploee']['duration_of_probation_id'],
                                         reply_markup=create_inline_kb('add_new_duration',
                                                                       'back_to_have_probation_or_not',
                                                                       'cancel_all', width=1, **get_duration()))
        await state.set_state(FSMemploee.duration_of_probation_id)

    elif data.get('chose_value', 0):
        await callback.message.edit_text(text=LEXICON_RU['upd_del_row_employee']['upd_duration_of_probation'],
                                         reply_markup=create_inline_kb('add_new_duration', 'back_to_upd_actions',
                                                                       'cancel_all', **get_duration()))
        await state.set_state(FSMemploee.upd_duration_of_probation)

    print(await state.get_state())
    print(await state.get_data())
