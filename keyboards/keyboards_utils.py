
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from lexicon.lexicon_ru import BUTTONS

########
#Делаем клавиатуру для выбора таблиц
from aiogram.utils.keyboard import InlineKeyboardBuilder

emploee_button = InlineKeyboardButton(text='Сотрудники', callback_data='employee')
position_tab_button = InlineKeyboardButton(text='Должности', callback_data='position_tab')
duration_of_probation_button = InlineKeyboardButton(text='Испытательные сроки', callback_data='duration_of_probation')
salary_button = InlineKeyboardButton(text='Зарплаты', callback_data='salary')
city_of_residence_button = InlineKeyboardButton(text='Города', callback_data='city_of_residence')


 # Добавляем кнопки в клавиатуру (две в одном ряду и одну в другом)
keyboard_tabs: list[list[InlineKeyboardButton]] = [[emploee_button, position_tab_button],
                                                   [salary_button, city_of_residence_button],
                                                   [duration_of_probation_button]]
# Создаем объект инлайн-клавиатуры
keyboard_tabs_markup = InlineKeyboardMarkup(inline_keyboard=keyboard_tabs)
##########






#### Функция создания клавиатуры
def create_inline_kb(*args, width: int=1, **kwargs) -> InlineKeyboardMarkup:
    # Инициализируем билдер
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    # Инициализируем список для кнопок
    buttons: list[InlineKeyboardButton] = []

    # Заполняем список кнопками из аргументов args и kwargs
    if kwargs:
        for button, text in kwargs.items():
            buttons.append(InlineKeyboardButton(
                text=text,
                callback_data=button))
    if args:
        for button in args:
            buttons.append(InlineKeyboardButton(
                text=BUTTONS[button] if button in BUTTONS else button,
                callback_data=button))
    # Распаковываем список с кнопками в билдер методом row c параметром width
    kb_builder.row(*buttons, width=width)

    # Возвращаем объект инлайн-клавиатуры
    return kb_builder.as_markup()



def create_inline_kb_arg(width: int,
                     *args: str) -> InlineKeyboardMarkup:
    # Инициализируем билдер
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    # Инициализируем список для кнопок
    buttons: list[InlineKeyboardButton] = []

    # Заполняем список кнопками из аргументов args и kwargs
    if args:
        for button in args:
            buttons.append(InlineKeyboardButton(
                text=BUTTONS[button] if button in BUTTONS else button,
                callback_data=button))


    # Распаковываем список с кнопками в билдер методом row c параметром width
    kb_builder.row(*buttons, width=width)

    # Возвращаем объект инлайн-клавиатуры
    return kb_builder.as_markup()