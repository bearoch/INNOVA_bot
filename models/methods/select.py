from datetime import timedelta, datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.models import PositionTab, DurationOfProbation, CityOfResidence, EmployeePosition, \
    Employee, SalaryHistory
from config_data.config import load_config, Config

config: Config = load_config('.env')
engine = create_engine(f'postgresql://{config.db.db_user}:{config.db.db_password}@{config.db.db_host}/{config.db.database}', echo=True)

session = sessionmaker(bind=engine)
s = session()


def get_positions(name_pos='', hold_pos: list=[]):
    positions = {}

    if hold_pos:
        try:
            for position_id, name_position in s.query(PositionTab.position_id, PositionTab.name_position):
                if name_position.lower() in ''.join(hold_pos).lower():
                    positions[str(position_id)] = name_position
            print(positions)
            return positions
        except:
            print("Ошибка во время получения позиции")

    if name_pos:
        print(name_pos, type(name_pos))
        try:
            for position_id, name_position in s.query(PositionTab.position_id, PositionTab.name_position):
                print(position_id, type(position_id))
                if (name_pos.isalpha() and name_pos.lower() in name_position.lower()) or (name_pos.isdigit() and int(name_pos) == position_id):

                    positions[str(position_id)] = name_position
            print(positions)
            return positions
        except:
            print("Ошибка во время получения позиции")

    return positions


def get_duration():
    duration: dict = {}
    try:
        for id, dur in s.query(DurationOfProbation.duration_of_probation_id, DurationOfProbation.duration_of_probation):
            duration[str(id)] = dur
        print(duration)
        return dict(sorted(duration.items(), key=lambda item: int(item[1])))
    except:
        print("Ошибка во время получения позиции")
    return duration


def get_cityes(name_city: str = ''):
    city = {}
    if not name_city:
        try:
            for id, c in s.query(CityOfResidence.city_of_residence_id, CityOfResidence.name_city):
                city[str(id)] = c
        except:
            print("Ошибка во время получения города")
        print(city)
    if name_city:
        try:
            for id, c in s.query(CityOfResidence.city_of_residence_id, CityOfResidence.name_city):
                if name_city.isalpha() and name_city.lower() in c.lower() or name_city.isdigit() and int(
                        name_city) == id:
                    city[str(id)] = c
        except:
            print("Ошибка во время получения города по названию")

    return city


def get_list_employees():
    new_dict = {}
    try:
        for id, name in s.query(Employee.employee_id, Employee.name_employee):
            new_dict[str(id)] = name
    except:
        print("Ошибка во время получения списка сотрудников")

    return new_dict


def get_employee(name_emp: str, show_dismissed=False):
    new_dict = {}
    try:
        for id, name, dismissal in s.query(Employee.employee_id, Employee.name_employee, Employee.date_of_dismissal):
            print(id, name, dismissal)
            if show_dismissed:
                if name_emp.isalpha() and name_emp.lower() in name.lower() or name_emp.isdigit() and int(name_emp) == id:
                    new_dict[str(id)] = name
            else:
                if dismissal == None and (name_emp.isalpha() and name_emp.lower() in name.lower() or name_emp.isdigit() and int(name_emp) == id):
                    new_dict[str(id)] = name

    except:
        print("Ошибка во время получения города имени сотрудника")

    return new_dict


def information_about_employee(employee_id: dict):
    new_d = {}

    try:
        for row in s.query(Employee, DurationOfProbation,
                           CityOfResidence).where(Employee.employee_id == int(employee_id['employee_id'])).filter(
            Employee.city_of_residence_id == CityOfResidence.city_of_residence_id,
            Employee.duration_of_probation_id == DurationOfProbation.duration_of_probation_id):
            if row.Employee.date_of_dismissal != None:
                new_d['upd_0_dismissed'] = f'Уволен - {row.Employee.date_of_dismissal.strftime("%d.%m.%Y")}'
            if row.Employee.have_duration_of_probation == "Да":
                new_d['upd_1_name'] = f'ФИО: {row.Employee.name_employee}'
                new_d['upd_3_date_empl'] = f'Дата устройства: {row.Employee.date_of_employment.strftime("%d.%m.%Y")}'
                new_d['upd_4_salary_on_probation'] = f'Оклад во время ИС: {row.Employee.salary_on_probation} руб.'
                new_d[
                    'upd_6_duration_of_probation'] = f'Продолжительность ИС: {row.DurationOfProbation.duration_of_probation} дней'
                date_end_duration_of_probation = row.Employee.date_of_employment + timedelta(
                    days=int(row.DurationOfProbation.duration_of_probation))
                new_d[
                    'upd_7_date_finish_duration'] = f'Дата завершения ИС: {date_end_duration_of_probation.strftime("%d.%m.%Y")}'
                new_d['upd_8_city_of_residence'] = f'Город проживания: {row.CityOfResidence.name_city}'
                new_d['upd_9_phone_number'] = f'Телефонный номер: {row.Employee.phone_number}'
                new_d['upd_99_date_of_birth'] = f'Дата рождения: {row.Employee.date_of_birth.strftime("%d.%m.%Y")}'
    except:
        print('Ошибка во время формирования информации о сотруднике с ИС')

    try:
        for row in s.query(Employee, CityOfResidence).where(Employee.employee_id == int(employee_id['employee_id'])).filter(
            Employee.city_of_residence_id == CityOfResidence.city_of_residence_id):
            print(row.Employee.have_duration_of_probation)
            if row.Employee.date_of_dismissal != None:
                new_d['upd_0_dismissed'] = f'Уволен - {row.Employee.date_of_dismissal.strftime("%d.%m.%Y")}'
            if row.Employee.have_duration_of_probation == "Нет":
                print(2)
                new_d['upd_1_name'] = f'ФИО: {row.Employee.name_employee}'
                new_d['upd_3_date_empl'] = f'Дата устройства: {row.Employee.date_of_employment.strftime("%d.%m.%Y")}'
                new_d['upd_8_city_of_residence'] = f'Город проживания: {row.CityOfResidence.name_city}'
                new_d['upd_9_phone_number'] = f'Телефонный номер: {row.Employee.phone_number}'
                new_d['upd_99_date_of_birth'] = f'Дата рождения: {row.Employee.date_of_birth.strftime("%d.%m.%Y")}'

    except:
        print('Сделать выборку из таблицы сотрудники не получилось')

    try:
        salary_history = get_salary_history(employee_id['employee_id'])
        # salary_history[date]=f'Зарплата сотрудника {salar} руб.'
        new_d['upd_5_salary'] = f'Зарплата сотрудника {max(salary_history.items(), key=lambda x: x[0])[1]} руб.'
    except:
        print("Выгрузить историю зарплат не получилось, функция information_about_employee")

    try:
        position_history = get_position_history(employee_id['employee_id'])
        new_d['upd_2_position'] = f'Должность: {max(position_history.items(), key=lambda x: x[0])[1]}'

    except:
        print("Выгрузить историю должностей не получилось, функция information_about_employee")

    print(new_d)
    return dict(sorted(new_d.items()))






def get_colum_from_emploee(table: str):
    if table == 'position_tab':
        new_dict = {}
        for id, pos_id in s.query(Employee.employee_id, Employee.position_id):
            new_dict[id] = pos_id
        positions = set()
        positions.update(new_dict.values())
        return positions
    elif table == 'salary':
        new_dict = {}
        for id, sal_id in s.query(Employee.employee_id, Employee.salary):
            new_dict[id] = sal_id
        salar = set()
        salar.update(new_dict.values())
        return salar
    elif table == 'city_of_residence':
        new_dict = {}
        for id, cit_id in s.query(Employee.employee_id, Employee.city_of_residence_id):
            new_dict[id] = cit_id
        city = set()
        city.update(new_dict.values())
        return city
    elif table == 'duration_of_probation':
        new_dict = {}
        for id, dur_id in s.query(Employee.employee_id, Employee.duration_of_probation_id):
            new_dict[id] = dur_id
        duration = set()
        duration.update(new_dict.values())
        return duration




# Сначала сделать поиск всех последних позиций сотрудников, а потом взять нужные из этого списка
def get_information_by_categoryes(category='', id=''):
    result = {}
    if category == 'positions':
        try:
            all_names: dict = {}
            for row in s.query(EmployeePosition, Employee).filter(Employee.employee_id==EmployeePosition.employee_id):
                if not row.Employee.date_of_dismissal:
                    all_names[row.Employee.name_employee] = [row.EmployeePosition.position_id, row.EmployeePosition.date_of_change]

            for k, v in all_names.items():
                if v[0] == int(id):
                    result[k] = f'{k} - c {v[1].strftime("%d.%m.%Y")}'
            print(result)
        except:
            print('Ошибка получения информации в категории по должностям')
        return result

    elif category == 'cities':
        try:
            for row in s.query(Employee):
                if row.city_of_residence_id == int(id) and not row.date_of_dismissal:
                   result[row.employee_id] = row.name_employee
        except:
            print('Ошибка во время получения информации в категории по городам')

    elif category == 'birthday':
        new = {}
        try:
            next_months = datetime.now() + timedelta(days=90)
            closest_date: list = [datetime.fromordinal(i) for i in
                                  range(datetime.now().toordinal(), next_months.toordinal())]
            for i in closest_date:
                for row in s.query(Employee):
                    if row.date_of_birth.strftime('%d.%m') == i.strftime('%d.%m') and not row.date_of_dismissal:
                        new[row.name_employee] = i.strftime('%d.%m.%Y')

            for k, v in new.items():
                result[k] = f'{k} - {v}'
        except:
            print('Ошибка во время получения информации по дням рождений')
        return result

    elif category == 'duration':
        new: dict = {}
        try:
            for row in s.query(Employee, DurationOfProbation).where(Employee.have_duration_of_probation=='Да').filter(Employee.duration_of_probation_id==DurationOfProbation.duration_of_probation_id):
                if not row.Employee.date_of_dismissal:
                    new[row.Employee.name_employee] = timedelta(days=row.DurationOfProbation.duration_of_probation) + row.Employee.date_of_employment

            for k, v in sorted(new.items(), key=lambda x: x[1]):
                if v > datetime.now().date():
                    result[k] = f'{k} - {v.strftime("%d.%m.%Y")}'

        except:
            print('Ошибка во время получения информации в категории по ИС')
        return result
    return dict(sorted(result.items()))


# Выводит историю должностей конкретного сотрудника
def get_position_history(emp_id):
    try:
        position_history = {}
        for row in s.query(EmployeePosition, PositionTab).where(EmployeePosition.employee_id == int(emp_id)).filter(
                EmployeePosition.position_id == PositionTab.position_id):
            position_history[row.EmployeePosition.date_of_change] = row.PositionTab.name_position
        print(position_history)
        return position_history
    except:
        print('Получить историю должностей не вышло "get_position_history"')


def get_salary_history(emp_id):
    try:
        salary_history = {}
        for id, salary, date in s.query(SalaryHistory.employee_id, SalaryHistory.salary, SalaryHistory.date_of_change):
            if str(id) == emp_id:
                salary_history[date] = salary
        return salary_history
    except:
        print('Получить историю зарплат не вышло "get_salary_history"')


