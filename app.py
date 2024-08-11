from flask import Flask, url_for, render_template, json, session, redirect

from blueprint_auth.route import blueprint_auth
from blueprint_query.route import blueprint_query
from blueprint_basket.route import blueprint_order
from blueprint_report.route import blueprint_report
from blueprint_verification.route import blueprint_verification
from blueprint_order_status.route import blueprint_order_st
from blueprint_order_history.route import blueprint_order_history
from blueprint_menu.route import blueprint_menu


from access import login_required

app = Flask(__name__)
app.secret_key = 'restoran'
#Чтобы использовать сессии/сеансы, необходимо установить секретный ключ, при помощи которого будут подписываться сессионные cookie.

#Если установлен атрибут экземпляра приложения Flask.secret_key или настроен параметр конфигурации SECRET_KEY,
# то можно использовать сессии/сеансы в приложениях Flask. Сессия/сеанс Flask позволяет запоминать информацию от одного запроса к другому.
# Фреймворк Flask делает это с помощью подписанного файла cookie. Пользователь может просматривать содержимое сессии/сеанса,
# но не может изменять его, если не знает секретный ключ, поэтому обязательно установите для него что-то сложное.


app.register_blueprint(blueprint_auth, url_prefix='/auth')
app.register_blueprint(blueprint_query, url_prefix='/requests')
app.register_blueprint(blueprint_order, url_prefix='/order')
app.register_blueprint(blueprint_report, url_prefix='/report')
app.register_blueprint(blueprint_verification, url_prefix='/verification')
app.register_blueprint(blueprint_order_st, url_prefix='/order_status')
app.register_blueprint(blueprint_order_history, url_prefix='/order_history')
app.register_blueprint(blueprint_menu, url_prefix='/menu_editting')

app.config['db_config'] = json.load(open('data_files/dbconfig.json'))
app.config['access_config'] = json.load(open('data_files/access.json'))

@app.route('/', methods=['GET', 'POST'])
@login_required
def menu_choice():
    if 'user_id' in session:
        if session.get('user_group', 'external'):
            return render_template('internal_user_menu.html')
        else:
            return render_template('external_user_menu.html')
    else:
        return redirect(url_for('blueprint_auth.start_auth'))
# session - словароподобный объект
#Метод Session.get() возвращает значение для ключа сессии/сеанса key (если он есть),
#иначе возвращается значение по умолчанию default.

@app.route('/exit')
def exit_func():
    if 'user_id' in session:
        session.pop('user_id')
    if 'user_group' in session:
        session.pop('user_group')
    return redirect(url_for('menu_choice'))

#Метод Session.pop() удаляет указанный ключ сессии/сеанса key и возвращает соответствующее значение.


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=9002)
