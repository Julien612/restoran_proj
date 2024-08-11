from flask import *
from functools import wraps

#func = login_required(func)
#func() => wrapper()
#проверка на наличие аккаунта
def login_required(func):
    @wraps(func) # Заменяет атрибуты декоратора на атрибуты исходной функции.
    def wrapper(*args, **kwargs):
        if 'user_id' in session:
            return func(*args, **kwargs)
        return redirect(url_for("blueprint_auth.start_auth"))
    return wrapper

#validation - подтверждение группы доступа
def group_validation(config: dict) -> bool:
    endpoint_func = request.endpoint
    #Свойство Request.endpoint представляет собой конечную точку, соответствующую URL-адресу запроса.
    #Это свойство будет возвращать None, если сопоставление URL-адреса не удалось или еще не было выполнено
    print('endpoint_func=', endpoint_func)
    endpoint_app = request.endpoint.split('.')[0]
    print('endpoint_app=', endpoint_app)
    if 'user_group' in session:
        user_group = session['user_group']
        if user_group in config and endpoint_app in config[user_group]:
            return True
        elif user_group in config and endpoint_func in config[user_group]:
            return True
    return False

# f = group_required(f)
# f() -> wrapper()
# проверка на существование группы доступа, если проверка не пройдена - отказ в доступе
def group_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        config = current_app.config['access_config']
        if group_validation(config):
            return f(*args, **kwargs)
        return render_template('access_refused.html')
    return wrapper