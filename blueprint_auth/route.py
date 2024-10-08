import os
from typing import Optional, Dict

from flask import Blueprint, request, render_template, current_app, session, redirect, url_for
from db_work import select_dict
from sql_provider import SQLProvider

blueprint_auth = Blueprint('blueprint_auth', __name__, template_folder='templates')
provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))


@blueprint_auth.route('/', methods=['GET', 'POST'])
def start_auth():
    if request.method == 'GET':
        return render_template('input_login.html')
    else:
        login = request.form.get('login') #Свойство request.form возвращает данные полей переданной HTML-формы
        password = request.form.get('password')
        if login:
            user_info = define_user(login, password)
            if user_info:
                user_dict = user_info[0]
                # в сессию заносятся айди и группа пользователя если он существует в базе
                session['user_id'] = user_dict['user_id']
                session['user_group'] = user_dict['user_group']
                session.permanent = True
                # Атрибут сессии/сеанса Session.permanent отвечает за время жизни сессии/сеанса.
                # Если установлено значение True, то сессия/сеанс существует в течение app.permanent_session_lifetime секунд.
                # По умолчанию 31 день. Если установлено значение False (по умолчанию), то сессия/сеанс будет удалена,
                # когда пользователь закроет браузер.
                return redirect(url_for('menu_choice'))
            else:
                return render_template('input_login.html', message='Пользователь не найден')
        return render_template('input_login.html', message='Повторите ввод')

#define_user возвращает user_id и user_group в виде словаря
def define_user(login: str, password: str) -> Optional[Dict]:
    sql_internal = provider.get('internal_user.sql', login=login, password=password)
    sql_external = provider.get('external_user.sql', login=login, password=password)

    user_info = None

    for sql_search in [sql_internal, sql_external]:
        _user_info = select_dict(current_app.config['db_config'], sql_search)
        print('_user_info=', _user_info)
        if _user_info:
            user_info = _user_info
            del _user_info
            break
    return user_info
