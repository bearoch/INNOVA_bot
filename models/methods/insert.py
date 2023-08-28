from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.models import PositionTab, DurationOfProbation, CityOfResidence, Employee, \
    EmployeePosition, SalaryHistory

from config_data.config import Config, load_config

config: Config = load_config('.env')
engine = create_engine(f'postgresql://{config.db.db_user}:{config.db.db_password}@{config.db.db_host}/{config.db.database}', echo=True)


session = sessionmaker(bind=engine)
s = session()


class InsertInto:

    def position_tab_insert_row(values: dict):
        try:
            row = PositionTab(name_position=values['name_position'])
            s.add(row)
            s.commit()
        except:
            print("Ошибка во время выполнения добавления новой строки в таблицу позиции")

    def duration_of_probation_row(values: dict):
        try:
            row = DurationOfProbation(duration_of_probation=values['new_duration'])
            s.add(row)
            s.commit()
        except:
            print(
                "Ошибка во время выполнения добавления новой строки в продолжительность ИС 'duration_of_probation_row'")

    #    def salary_row(values: dict):
    #        row = salary(salary=values['salary'])
    #        s.add(row)
    #        s.commit()

    def city_of_residence_row(values: dict):
        row = CityOfResidence(name_city=values['name_city'])
        s.add(row)
        s.commit()

    def employee_insert_row(values: dict):
        try:
            row = Employee(name_employee=values['name_employee'],
                           date_of_employment=values['date_of_employment'],
                           salary_on_probation=values.get('salary_on_probation', None),
                           have_duration_of_probation=values['answer_probation'],
                           duration_of_probation_id=values.get('duration_of_probation_id', None),
                           city_of_residence_id=values['city_of_residence_id'],
                           phone_number=values['phone_number'],
                           date_of_birth=values['date_of_birth'])
            s.add(row)
            s.commit()
        except:
            print('Ошибка во время выполнения добавления нового сотрудника в таблицу сотрудники "employee_insert_row"')



    def employee_position_row(values: dict):
        try:
            if values.get('employee_id', 0) == 0:
                for id, name in s.query(Employee.employee_id, Employee.name_employee):
                    if name == values['name_employee']:
                        values['employee_id'] = str(id)
        except:
            print('ID сотрудника в функции "employee_position_row" не найдено')

        try:
            row = EmployeePosition(employee_id=values['employee_id'], position_id=values['position_id'])
            s.add(row)
            s.commit()
        except:
            print('Новая строка не добавлена в "EmployeePosition"')




    def salary_history_row(values: dict):

        try:
            for id, name in s.query(Employee.employee_id, Employee.name_employee):
                if name == values['name_employee']:
                    values['employee_id']= str(id)
        except:
            print('ID сотрудника в функции "salary_history_row" не найдено')

        try:
            row = SalaryHistory(employee_id=values['employee_id'], salary=values['salary'])
            s.add(row)
            s.commit()
        except:
            print('Новая строка не добавлена в "salary_history_row" не найдено')
