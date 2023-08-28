
from sqlalchemy.orm import sessionmaker
from models.models import Employee
from sqlalchemy import update, create_engine
from config_data.config import Config, load_config

config: Config = load_config('.env')
engine = create_engine(f'postgresql://{config.db.db_user}:{config.db.db_password}@{config.db.db_host}/{config.db.database}', echo=True)

session = sessionmaker(bind=engine)
s = session()

def update_employee(column: str, new_value: dict):
    if column == 'name_employee':
        stmt = (update(Employee).where(Employee.employee_id == int(new_value['employee_id'])).values(name_employee=new_value['upd_new_name_emp']))
    elif column == 'date_of_employment':
        stmt = (update(Employee).where(Employee.employee_id == int(new_value['employee_id'])).values(date_of_employment=new_value['upd_new_date_of_employment']))
    elif column == 'date_of_dismissal':
        stmt = (update(Employee).where(Employee.employee_id == int(new_value['employee_id'])).values(date_of_dismissal=new_value['date_of_dismissal']))
    elif column == 'salary_on_probation':
        stmt = (update(Employee).where(Employee.employee_id == int(new_value['employee_id'])).values(salary_on_probation=new_value['upd_new_salary_on_probation']))
    elif column == 'duration_of_probation_id':
        stmt = (update(Employee).where(Employee.employee_id == int(new_value['employee_id'])).values(duration_of_probation_id=new_value['upd_duration_of_probation']))
    elif column == 'city_of_residence_id':
        stmt = (update(Employee).where(Employee.employee_id == int(new_value['employee_id'])).values(city_of_residence_id=new_value['upd_city_of_residence']))
    elif column == 'phone_number':
        stmt = (update(Employee).where(Employee.employee_id == int(new_value['employee_id'])).values(phone_number=new_value['upd_new_phone_number']))
    elif column == 'date_of_birth':
        stmt = (update(Employee).where(Employee.employee_id == int(new_value['employee_id'])).values(date_of_birth=new_value['upd_new_date_of_birth']))


    s.execute(stmt)
    s.commit()