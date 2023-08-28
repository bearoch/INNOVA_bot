import asyncio
import logging
from aiogram import Bot, Dispatcher
from sqlalchemy import create_engine

from config_data.config import Config, load_config
from handlers import main_handlers, other_handlers

from aiogram.fsm.storage.redis import RedisStorage, Redis, DefaultKeyBuilder

from handlers.export_to_excel_handlers import export_to_excel_handlers
from handlers.insert_handlers import employee_insert_into, position_tab_insert_into, duration_of_probation_insert_into, \
    city_of_residence_insert_into
from handlers.update_or_delete import emploee_upd_del, dismissal_employee
from handlers.select_handlers import employee_select, position_history, salary_history
from handlers.select_handlers.category_select import by_category
from keyboards.set_menu import set_main_menu

logger = logging.getLogger(__name__)

# Инициализируем Redis
redis: Redis = Redis(host='localhost')

# Инициализируем хранилище (создаем экземпляр класса RedisStorage)
storage: RedisStorage = RedisStorage(redis=redis, key_builder=DefaultKeyBuilder(with_destiny=True))

# Загружаем конфиг в переменную config
config: Config = load_config('.env')

# Функция конфигурирования и запуска бота
async def main() -> None:

    # Конфигурируем логирование
    logging.basicConfig(
        level=logging.INFO,
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
               '[%(asctime)s] - %(name)s - %(message)s')

    # Выводим в консоль информацию о начале запуска бота
    logger.info('Starting bot')


    # Инициализируем бот и диспетчер

    bot: Bot = Bot(token=config.tg_bot.token)
    dp: Dispatcher = Dispatcher(storage=storage)

    # Инициализируем кнопки меню
    await set_main_menu(bot)


    # Регистрируем роутеры
    dp.include_router(main_handlers.router)
    dp.include_router(employee_select.router)
    dp.include_router(position_tab_insert_into.router)
    dp.include_router(duration_of_probation_insert_into.router)
    dp.include_router(city_of_residence_insert_into.router)
    dp.include_router(employee_insert_into.router)
    dp.include_router(emploee_upd_del.router)
    dp.include_router(dismissal_employee.router)
    dp.include_router(by_category.router)
    dp.include_router(position_history.router)
    dp.include_router(salary_history.router)
    dp.include_router(export_to_excel_handlers.router)

    dp.include_router(other_handlers.router)

    # Пропускаем накопившиеся апдейты и запускаем polling
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
