from aiogram.filters import StateFilter, Text
from aiogram.fsm.context import FSMContext
from aiogram import Router, F
from aiogram.types import (CallbackQuery, Message)
from states.states import FSMemploee
from keyboards.keyboards_utils import create_inline_kb_arg, create_inline_kb
from models.methods.insert import InsertInto
from lexicon.lexicon_ru import LEXICON_RU
from filters.language_filter import CheckLenRowFilter, CheckUniqueFilter
from models.methods.select import get_positions

router: Router = Router()


@router.callback_query(StateFilter(FSMemploee.position_id), Text(text=['add_new_position']))
@router.callback_query(StateFilter(FSMemploee.upd_position), Text(text=['add_new_position']))
async def process_add_new_position(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await callback.message.answer(text=LEXICON_RU['add_row_emploee']['add_new_position'],
                                  reply_markup=create_inline_kb('back_to_choose_position'))
    await state.set_state(FSMemploee.name_position)
    await callback.answer(text=LEXICON_RU['callback.answers']['go'])
    print(await state.get_state())
    print(await state.get_data())


@router.message(StateFilter(FSMemploee.name_position), F.content_type == 'text', CheckLenRowFilter(row_len=100),
                CheckUniqueFilter(table_values=get_positions()))
async def process_add_new_position(message: Message, state: FSMContext):
    await state.update_data(name_position=message.text)
    data = await state.get_data()
    await message.answer(text=f'Подтвердите указанную ранее информацию:\n'
                              f'Должность - {data["name_position"]}',
                         reply_markup=create_inline_kb('yes', 'no', width=1))
    await state.set_state(FSMemploee.approve_position)
    print(await state.get_state())
    print(await state.get_data())


@router.callback_query(StateFilter(FSMemploee.approve_position))
async def process_add_approve(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    if callback.data == 'yes':
        InsertInto.position_tab_insert_row(await state.get_data())
        await callback.answer(text=LEXICON_RU['callback.answers']['finish_yes'], show_alert=True)

    else:
        await callback.answer(text=LEXICON_RU['callback.answers']['finish_no'], show_alert=True)
    # ----
    if data.get('chose_value', 0) == 0:
        await callback.message.edit_text(text=LEXICON_RU['add_row_emploee']['add_position'],
                                         reply_markup=create_inline_kb('back_to_name_emp', 'cancel_all',
                                                                       width=1, **get_positions(hold_pos=LEXICON_RU['add_row_emploee']['hold_positions'])))
        await state.set_state(FSMemploee.position_id)

    else:
        await callback.message.edit_text(text=LEXICON_RU['upd_del_row_employee']['upd_position'],
                                         reply_markup=create_inline_kb('back_to_upd_actions', 'cancel_all',
                                                                       **get_positions(hold_pos=LEXICON_RU['add_row_emploee']['hold_positions'])))
        await state.set_state(FSMemploee.upd_position)
    print(await state.get_state())
    print(await state.get_data())
