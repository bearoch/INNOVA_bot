
# Создаем "базу данных" пользователей

from aiogram.fsm.state import StatesGroup, State

user_dict: dict[int, dict[str, str | int | bool]] = {}


# Состояния при добавлении новых строк в таблицу сотрудников, обновления информации в ней и увольнении сотрудника
class FSMemploee(StatesGroup):
    choose_action = State()
    select_emp_actions = State()
    select_emp_category = State()
    name_employee = State()
    position_id = State()
    name_position = State()
    approve_position = State()
    date_of_employment = State()
    have_probation_or_not = State()
    salary_on_probation = State()
    duration_of_probation_id = State()
    new_duration = State()
    approve_duration = State()
    salary = State()
    city_of_residence_id = State()
    name_city = State()
    approve_city = State()
    phone_number = State()
    date_of_birth = State()
    approve = State()

    upd_dismissal_action = State()
    upd_name_emp = State()
    set_new_meaning = State()
    upd_name_for_upd = State()
    upd_approve_new_name = State()
    upd_position = State()
    upd_approve_new_position = State()
    upd_date_of_employment = State()
    upd_approve_new_date_of_employment = State()
    upd_salary_on_probation = State()
    upd_approve_salary_on_probation = State()
    upd_salary = State()
    upd_approve_salary = State()
    upd_duration_of_probation = State()
    upd_approve_new_duration_of_probation = State()
    upd_city_of_residence = State()
    upd_approve_new_city_of_residence = State()
    upd_phone_number = State()
    upd_approve_new_phone_number = State()
    upd_date_of_birth = State()
    upd_approve_new_date_of_birth = State()

    sel_name_emp = State()
    sel_show_emp_inf = State()
    category_position = State()
    category_cities = State()

    dis_name_emp = State()
    dis_approve_date = State()
    dis_approve_answer = State()



# Состояния при добавлении новых строк в таблицу должностей
class FSMpositions(StatesGroup):
    choose_action = State()
    name_employee = State()
    approve_name_emp = State()
    show_position_history = State()

class FSMsalary(StatesGroup):
    choose_action = State()
    name_employee = State()

    show_salary_history = State()