import datetime
from sqlalchemy import Column, ForeignKey, Integer, VARCHAR, DECIMAL, DATE, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from config_data.config import Config, load_config

config: Config = load_config('.env')
engine = create_engine(f'postgresql://{config.db.db_user}:{config.db.db_password}@{config.db.db_host}/{config.db.database}', echo=True)

Base = declarative_base()


def _get_date():
    return datetime.datetime.now()


class PositionTab(Base):
    __tablename__ = 'PositionTab'

    position_id = Column(Integer, primary_key=True)
    name_position = Column(VARCHAR(100), nullable=False)


    employee_position = relationship('EmployeePosition')


class DurationOfProbation(Base):
    __tablename__ = 'DurationOfProbation'

    duration_of_probation_id = Column(Integer, primary_key=True)
    duration_of_probation = Column(Integer)

    employee = relationship('Employee')


#class salary(Base):
#    __tablename__ = 'salary'
#
#    salary_id = Column(Integer, primary_key=True)
#    salary = Column(DECIMAL(10, 2), nullable=False)

#    employee = relationship('employee')
#    salary_history = relationship('salary_history')


class CityOfResidence(Base):
    __tablename__ = 'CityOfResidence'

    city_of_residence_id = Column(Integer, primary_key=True)
    name_city = Column(VARCHAR(40), nullable=False)

    employee = relationship('Employee')


class Employee(Base):
    __tablename__ = 'Employee'

    employee_id = Column(Integer, primary_key=True)
    name_employee = Column(VARCHAR(40), nullable=False)
    date_of_employment = Column(DATE, nullable=False)
    have_duration_of_probation = Column(VARCHAR(40), nullable=False)
    salary_on_probation = Column(DECIMAL(10, 2))
    duration_of_probation_id = Column(Integer, ForeignKey('DurationOfProbation.duration_of_probation_id'))
    city_of_residence_id = Column(Integer, ForeignKey('CityOfResidence.city_of_residence_id'))
    phone_number = Column(VARCHAR(11))
    date_of_birth = Column(DATE)
    date_of_dismissal = Column(DATE)
    date_of_create = Column(DateTime, default=_get_date)
    date_of_update = Column(DateTime, onupdate=_get_date)

    employee_position = relationship('EmployeePosition')
    duration_of_probation = relationship('DurationOfProbation')
    city_of_residence = relationship('CityOfResidence')
    salary_history = relationship('SalaryHistory')


class EmployeePosition(Base):
    __tablename__ = 'EmployeePosition'

    employee_position_id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey('Employee.employee_id'), nullable=False)
    position_id = Column(Integer, ForeignKey('PositionTab.position_id'), nullable=False)
    date_of_change = Column(DateTime, default=_get_date)

    employee = relationship('Employee')
    position_tab = relationship('PositionTab')


class SalaryHistory(Base):
    __tablename__ = 'SalaryHistory'

    salary_history_id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey('Employee.employee_id'), nullable=False)
    salary = Column(DECIMAL(10, 2))
    date_of_change = Column(DateTime, default=_get_date)

    employee = relationship('Employee')



Base.metadata.create_all(engine)