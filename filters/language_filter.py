from datetime import datetime

from aiogram.types import Message
from aiogram.filters import BaseFilter
from lexicon.lexicon_ru import LEXICON_RU, FILTER_FOULS


# Фильтр проверяет, является ли введенное значение цифрами и если нет, то меняет текст ошибки для хендлера
class CheckIsdigitFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        if message.text.isdigit():
            return True
        else:
            LEXICON_RU['fault_text'] = FILTER_FOULS['only_digit']
            return False


# Фильтр проверяет, является ли введенное значение строкой и состоит как минимум из 2 слов
# и если нет меняет текст ошибки для хендлера
class CheckNameFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool | dict[str, str]:
        x = message.text.split()
        new_name = {}
        for i in x:
            if not i.isalpha():
                LEXICON_RU['fault_text'] = FILTER_FOULS['not_alpha']
                return False
        if len(x) < 3:
            LEXICON_RU['fault_text'] = FILTER_FOULS['short_name']
            return False
        new_name['new_name'] = ' '.join(x).title()
        return new_name


# Фильтр проверяет, является ли введенное значение датой в формате ГГГГ.ММ.ДД
# и если нет, то меняет текст ошибки для хендлера
class CheckDateFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool | dict[str, str]:
        y = message.text
        q = message.text.split('.')

        d_now = str(datetime.now())[:10].split('-')
        flag = True
        if len(y) != 10:
            LEXICON_RU['fault_text'] = FILTER_FOULS['not_date']
            return False
        for i in y:
            for j in ' !@™£#№;$%©:^?&*₽()_-=+≠][`|?/«"<>≤≥,':
                if i == j:
                    LEXICON_RU['fault_text'] = FILTER_FOULS['not_point']
                    return False
                if not (i.isdigit() or i == '.'):
                    LEXICON_RU['fault_text'] = FILTER_FOULS['not_date']
                    return False

        x = [q[2], q[1], q[0]]
        if not len(x[0]) < 5:
            LEXICON_RU['fault_text'] = FILTER_FOULS['wrong_year']
            return False
        if not (len(x[1]) == 2 and int(x[1]) < 13):
            LEXICON_RU['fault_text'] = FILTER_FOULS['wrong_month']
            return False
        if not (len(x[2]) == 2 and int(x[2]) < 32):
            LEXICON_RU['fault_text'] = FILTER_FOULS['wrong_day']
            return False
        if x > d_now:
            LEXICON_RU['fault_text'] = FILTER_FOULS['big_date']
            return False
        new_date = {'new_date': '.'.join(x)}
        return new_date


class CheckCityFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:

        x = message.text
        flag = True
        for i in x:
            if not (i.isalpha() or i == '-'):
                LEXICON_RU['fault_text'] = FILTER_FOULS['not_alpha']
                flag = False
                return flag
        if message.text == '-':
            LEXICON_RU['fault_text'] = FILTER_FOULS['not_alpha']
            return False
        return flag


class CheckLenRowFilter(BaseFilter):

    def __init__(self, row_len: int) -> None:
        self.row_len = row_len

    async def __call__(self, message: Message) -> bool:
        x = message.text
        flag = True
        if len(x) > self.row_len:
            LEXICON_RU['fault_text'] = FILTER_FOULS['wrong_len']
            flag = False
            return flag

        return flag


class CheckUniqueFilter(BaseFilter):

    def __init__(self, table_values: dict) -> None:
        self.table_values = table_values

    async def __call__(self, message: Message) -> bool:
        if message.text in self.table_values.values():
            LEXICON_RU['fault_text'] = FILTER_FOULS['not_unique_value']
            return False

        return True
