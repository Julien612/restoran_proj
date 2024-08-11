import os
from flask import Blueprint, render_template, request, current_app, session, redirect, url_for
from db_work import select_dict, insert
from sql_provider import SQLProvider


blueprint_order_history = Blueprint('bp_order_history', __name__, template_folder='templates', static_folder='static')
provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))



@blueprint_order_history.route('/')
def index():
    user_id = session.get('user_id')
    sql = provider.get('select_user_order.sql', user_id=user_id)
    result = select_dict(current_app.config['db_config'], sql)
    list, m = create_list(result)
    return render_template('order_history.html', result=result, list=list, m=m)

def create_list(result: dict):
    id = result[0]['order_id']
    id_ = result[0]['order_id']
    o = 1
    m = len(result)
    list = [0] * m
    list[0] = o
    for i in range(m):
        if id != id_:
            o += 1
            id = id_
            list[i] = o
        if i < m - 1:
            id_ = result[i + 1]['order_id']
    return list, m