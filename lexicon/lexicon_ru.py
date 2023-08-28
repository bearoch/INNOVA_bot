LEXICON_RU = {'/start': 'Добро пожаловать в телеграмм бот\n '
                        'который имеет возможность добавлять\n'
                        'новых сотрудников в базу данных,\n'
                        'изменять её, либо получать выборку\n'
                        'в зависимости от указанных параметров.\n'
                        'Чтобы подробнее ознакомиться с\n'
                        'возможностями бота, нажмите /help',
              '/help': 'В данном боте реализованно взаимодействие\n'
                       'с базой данных сотрудников.\n'
                       'Вам доступны следующие команды:\n'
                       '/add_row - позволяет добавить новые строки\n'
                       'в таблицы базы данных;\n'
                       '/select - позволяет вывести из таблиц\n'
                       'информацию о сотрудниках по выбранным\n'
                       'параметрам;\n'
                       '/update - позволяет внести изменения\n'
                       'в таблицы базы данных или удалить из них\n'
                       'выбранные значения;\n'
                       '/cancel - отменяет текущую операцию и удаляет\n'
                       'уже введенные значения',
              'not_admin': 'У вас нет полномочий пользоваться данным ботом(',
              'start': 'Привет, выберите таблицу с которой хотите работать!',
              'start_emp': 'Выберите действие, которое хотите осуществить с таблицей!',
              'select_emp': 'Вы можете посмотреть информацию об отдельном сотруднике,'
                            'или о нескольких, объединенных по определенным критериям',
              'category': 'Выберите категорию:',
              'category_duration': 'Доступные действия:',

              'cansel_if_yes': 'Вы прервали текущее действие,\n'
                               'выберете команду:\n\n'
                               '/add_row\n'
                               '/select\n'
                               '/update',
              'cansel_if_no': 'Отменять нечего, доступные команды:\n\n'
                              '/start\n'
                              '/help',

              'last': 'К сожалению бот не знает как\n'
                      'реагировать на ваше сообщение,\n'
                      'следуйте инструкции или выберите\n'
                      'команду из меню.',
              'fault_text': 'Введенное значение не принято, попробуйте еще раз',
              'callback.answers': {'go': 'Начинаем!',
                                   'success': 'Успешно! Продолжаем...',
                                   'finish_yes': 'Готово!',
                                   'finish_no': 'Операция отменена!'
                                   },
              'add_row_emploee': {'name': 'Введите ФИО сотрудника',
                                  'add_position': 'Выберите должность',
                                  'add_new_position': 'Введите название новой позиции:',
                                  'found_positions': 'Выберите должность сотрудника или повторите ввод',
                                  'repeat_pos': 'К сожалению должность не найдена, повторите ввод или нажмите на кнопу'
                                            '"Добавить новую должность"',
                                  'hold_positions': ['Python разработчик', 'SQL разработчик'],
                                  'date_of_employment': 'Укажите дату приема\nсотрудника на работу\nв формате ДД.ММ.ГГГГ',
                                  'have_probation_or_not': 'Установить сотруднику испытательный срок?',
                                  'salary_on_probation': 'Введите объем зарплаты во время испытательного срока, '
                                                         'например - 10000',
                                  'duration_of_probation_id': 'Выберите продолжительность испытательного срока.',
                                  'add_duration': 'Введите количество дней испытательного срока:',
                                  'salary_without_probation': 'Укажите размер зарплаты сотрудника:',
                                  'salary': 'Укажите размер зарплаты сотрудника после испытательного срока.',
                                  'city_of_residence_id': 'Выберете город, или введите название города в строке '
                                                          'для ввода',
                                  'name_city': 'Введите название города в котором\n'
                                                         'может проживать сотрудник:',
                                  'repeat': 'К сожалению город не найден, повторите ввод или нажмите на кнопу'
                                            '"Добавить новый город"',
                                  'found_cities': 'Выберите город проживания сотрудника или повторите ввод',
                                  'phone_number': 'Введите номер телефона сотрудника в формате 9992223344.',
                                  'date_of_birth': 'Введите дату рождения сотрудника в формате ДД.ММ.ГГГГ',
                                  'finish_yes': 'Информация о сотруднике успешно добавлена в БД',
                                  'finish_no': 'Операция по добавлению нового сотрудника в БД отменена!',

                                  },
              'upd_del_row_employee': {'upd_or_del': 'Изменить информацию о сотруднике, либо поставить отметку об '
                                                     'увольнении',
                                       'name_employee': 'Введите ФИО сотрудника, либо его ID.',
                                       'choose_emp_from_list': 'Выберите необходимого сотрудника из перечисленных ниже:',
                                       'repeat': 'К сожалению сотрудник не найден, повторите ввод',
                                       'actions': 'Выберите позицию, которую хотите изменить:',
                                       'upd_name_emp': 'Введите измененное имя сотрудника:',
                                       "upd_position": "Выберите новую должность для сотрудника или введите начало ее "
                                                       "названия",
                                       'found_positions': 'Выберите новую должность сотрудника или повторите ввод',
                                       'repeat_pos': 'К сожалению должность не найдена, повторите ввод или нажмите '
                                                     'на кнопу "Добавить новую должность"',
                                       'upd_date_empl': 'Введите новое значение в формате ДД.ММ.ГГГГ:',
                                       'upd_salary_on_probation': 'Введите новое значение зарплаты во время ИС:',
                                       'upd_salary': 'Введите новое значение зарплаты сотрудника:',
                                       'upd_duration_of_probation': 'Выберите количество дней ИС',
                                       'upd_city_of_residence': 'Выберите новый город из списка или введите название '
                                                                'нового города',
                                       'repeat_city': 'К сожалению город не найден, повторите ввод или нажмите на кнопу'
                                                      '"Добавить новый город"',
                                       'found_cities': 'Выберите город проживания сотрудника или повторите ввод',
                                       'upd_phone_number': 'Введите новый телефонный номер сотрудника',
                                       'upd_date_of_birth': 'Введите дату рождения в формате ДД.ММ.ГГГГ',
                                       },
              'dismissal_employee': {'name_employee': 'Введите ФИО сотрудника, либо его ID:',
                                     'choose_emp': 'Выберите необходимого сотрудника из перечисленных ниже:',
                                     'repeat': 'К сожалению сотрудник не найден, повторите ввод:',
                                     'add_date': 'Введите дату увольнения в формате ДД.ММ.ГГГГ\n'
                                                 'Сотрудник - ',
                                     },
              'select_employee': {'name_employee': 'Введите ФИО сотрудника, либо его ID.',
                                  'choose_emp_from_list': 'Выберите необходимого сотрудника из перечисленных ниже:',
                                  'repeat': 'К сожалению сотрудник не найден, повторите ввод',
                                  'name_position': 'Вы можете получить информацию о сотрудниках находящихся на '
                                                   'определенной должности.\n'
                                                   'Выберите должность или введите значение для поиска.',
                                  'found_positions': 'Выберите должность сотрудника или повторите ввод',
                                  'repeat_pos': 'К сожалению должность не найдена, повторите ввод',
                                  'repeat_search_pos': 'На данной позиции нет ни одного сотрудника',
                                  'name_city': 'Вы можете получить информацию о сотрудниках проживающих в определенном'
                                               ' городе.\n'
                                                   'Выберите город или введите значение для поиска.',
                                  'found_cities': 'Выберите город проживания сотрудника или повторите ввод',
                                  'repeat_cities': 'К сожалению город не найден, повторите ввод',
                                  'repeat_search_cities': 'В этом городе не проживает ни одного сотрудника',
                                  'not_birthdays': 'В ближайшие 3 месяца нет дней рождений сотрудников',
                                  'not_duration': 'Нет сотрудников находящихся на ИС',
                                  'cant_export_all_employs': 'Не удалось выгрузить полный список сотрудников',
                                  'cant_export_employs_on_probation': 'Не удалось выгрузить список сотрудников на ИС',
                                  'cant_export_dismissal_employs': 'Не удалось выгрузить список уволенных сотрудников',
                                  'cant_export_position_history': 'Не удалось выгрузить историю должностей сотрудников',
                                  'cant_export_salary_history': 'Не удалось выгрузить историю зарплат сотрудников',

                                  },
              'position_history': {'name_employee': 'Введите ФИО сотрудника, либо его ID:',
                                   'choose_emp_from_list': 'Выберите необходимого сотрудника из перечисленных ниже:',
                                   'repeat': 'К сожалению сотрудник не найден, повторите ввод',
                                   },
              'salary_history': {'name_employee': 'Введите ФИО сотрудника, либо его ID:',
                                 'choose_emp_from_list': 'Выберите необходимого сотрудника из перечисленных ниже:',
                                 'repeat': 'К сожалению сотрудник не найден, повторите ввод',
                                 },

              }



# Словари для клавиатур

MOVEMENTS_EMP: dict[str, str] = {
    'add_employee': 'Добавить нового сотрудника',
    'select_emp': 'Посмотреть информацию о сотрудниках',
    'update_emp': 'Изменить информацию о сотруднике',
    'back_to_start': 'Назад'
}

SELECT_EMP: dict[str, str] = {
    'employee_select': 'О конкретном сотруднике',
    'category': 'По категориям',
    'export_all_employees': 'Выгрузить список всех сотрудников',
    'export_all_dismissal_employees': 'Выгрузить список уволенных сотрудников',
    'back_to_emp_actions': 'Назад'
}

SELECT_EMP_CATEGORY: dict[str, str] = {

    'duration_of_probation_category': 'Информация о сотрудниках на ИС',
    'positions_category': 'По должностям',
    'cities_category': 'По городу проживания',
    'birthday_category': 'По ближайшим датам рождений',
    'back_to_select_emp_actions': 'Назад'
}

SELECT_EMP_ON_DURATION: dict[str, str] = {
    'all_employees_on_duration_of_probation': 'Выгрузить список сотрудников на ИС',
    'duration_of_probation_finish_soon': 'ИС заканчивается в ближайшее время',
    'back_to_movements_emp': 'Назад'
}

UPDATE_EMP: dict[str, str] = {
    'update_employee_information': 'Изменить информацию о сотруднике',
    'dismissal_employee': 'Уволить сотрудника',
    'back_to_emp_actions': 'Назад'
}

MOVEMENTS_POS: dict[str, str] = {
    'positions_history': 'Посмотреть историю должностей сотрудника',
    'export_position_history': 'Выгрузить историю должностей сотрудников',
    'back_to_start': 'Назад'
}

MOVEMENTS_SALARY: dict[str, str] = {
    'salary_history': 'Посмотреть историю зарплат сотрудника',
    'export_salary_history': 'Выгрузить историю зарплат сотрудников',
    'back_to_start': 'Назад'
}

LEXICON_COMMANDS_RU: dict[str, str] = {
    '/start': 'Начать работу с ботом.',
    '/help': 'Информация о возможностях бота.',
    '/cancel': 'Отменить текущее действие.'
}

TABLES: dict[str, str] = {
    'employee': 'Сотрудники',
    'positions': 'Должности',
    'salary': 'Зарплаты'
}




# Словарь для отдельных кнопок. Используются в функции create_inline_kb()
BUTTONS: dict[str, str] = {'yes': 'Да',
                           'no': 'Нет',
                           'del': 'Удалить',
                           'upd': 'Изменить',
                           'cancel_all': 'В главное меню',
                           'cancel_all_export': 'В главное меню',
                           'back_to_name_emp': "Назад",
                           'add_new_position': "Добавить новую должность",
                           'add_new_duration': 'Добавить новое значение',
                           'back_to_have_probation_or_not': 'Назад',
                           'back_to_salary_on_pron': "Назад",
                           'add_new_city': 'Добавить новый город',
                           'searcher_position': 'Вернуться к поиску должностей',
                           'searcher_city': 'Вернуться к поиску города',
                           'back_to_salary_without_probation':'Назад',
                           'back_to_salary_with_probation': 'Назад',
                           'back_to_salary': 'Назад',
                           'back_to_emp_actions': 'Назад',
                           'back_to_select_emp_actions': 'Назад',
                           'back_to_choose_position': 'Назад',
                           'back_to_date_employment': 'Назад',

                           'back_to_duration_of_prob': 'Назад',
                           'back_to_city': 'Назад',
                           'back_to_phone': 'Назад',
                           'back_to_date_of_birth': 'Назад',
                           'back_to_update_emp_actions': 'Назад',
                           'upd_back_to_name_emp': 'Вернуться к поиску сотрудника',
                           'sel_back_to_name_emp': 'Вернуться к поиску сотрудника',
                           'dismissal_back_to_name_emp': 'Вернуться к поиску сотрудника',
                           'back_to_add_date_dismissal': 'Назад',
                           'back_to_upd_actions': 'Назад к выбору позиции',
                           'back_to_changing_value': 'Назад',
                           'back_to_position_actions': 'Назад',
                           'pos_back_to_name_emp': 'Вернуться к поиску сотрудника',
                           'back_to_movements_emp': 'Назад',
                           'back_select_emp_on_duration_actions': 'Назад',

                           'back_to_salary_actions': 'Назад',
                           'salary_back_to_name_emp': 'Вернуться к поиску сотрудника'
                           }




# Словарь для ошибок. Используются в кастомных классах-фильтрах
FILTER_FOULS: dict = {'short_name': 'Введённые вами значение слишком короткое для данной позиции, повторите ввод.',
                      'not_alpha': 'Для данного поля возможно использование только букв и "-", повторите ввод.',
                      'only_digit': 'Для данного поля возможно использовать только цифры, повторите ввод.',
                      'not_point': 'Для данного поля в качестве разделителя возможно использовать только точку, '
                                   'повторите ввод',
                      'big_date': 'Внесенная дата больше текущей, проверьте введенное значение.',
                      'wrong_year': 'Год введен не корректно, проверьте значение и повторите ввод.',
                      'wrong_month': 'Месяц введен не корректно, проверьте значение и повторите ввод.',
                      'wrong_day': 'День введен не корректно, проверьте значение и повторите ввод.',
                      'not_date': 'Для указания даты используйте цифры разделенные точкой.',
                      'wrong_len': 'Длина введенной вами строки превышает установленное значение.\n'
                                   'Пожалуйста сократите строку.',
                      'not_unique_value': 'Введенное вами значение уже занесено в базу данных, введите новое значение!'
                      }
