import os

from flask import Blueprint, render_template, request, current_app, session, redirect, url_for
from db_context_manager import DBContextManager
from access import group_required
from db_work import select_dict, insert
from sql_provider import SQLProvider

blueprint_verification = Blueprint('bp_verification', __name__, template_folder='templates', static_folder='static')

provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))
a=0
order_id=0

@blueprint_verification.route('/',methods=['GET', 'POST'])#
@group_required
def verification():
    global a
    global order_id
    db_config = current_app.config['db_config']
    if request.method == 'GET':
        if order_id==0:
            _sql1 = provider.get('select_check_order_list.sql')
            items = select_dict(db_config, _sql1)
        else:
            _sql3 = provider.get('select_order_list_3.sql', order_id=order_id)
            items = select_dict(db_config, _sql3)
        basket_items = session.get('llist', {})
        print(basket_items)
        if a==0:
            a=1
            with DBContextManager(current_app.config['db_config']) as cursor:
                if cursor is None:
                    raise ValueError('Курсор не создан')
                else:
                    _sql2 = provider.get('set_status.sql', status='type3')
                    cursor.execute(_sql2)

        return render_template('ver.html', items=items, list=basket_items)
    else:
        dish_id = request.form['dish_id']
        _sql = provider.get('select_order_list_2.sql')

        with DBContextManager(db_config) as cursor:
            if cursor is None:
                raise ValueError('Cursor not found')
            cursor.execute(_sql)
            result = []  # список, каждый элемент которого является словарем
            schema = [column[0] for column in cursor.description]
            for row in cursor.fetchall():
                result.append(dict(zip(schema, row)))
        items = result
        add_to_list(dish_id, items)
        order_id=items[0]['order_id']
        return redirect(url_for('bp_verification.verification'))

def add_to_list(dish_id: str, items:dict):
    print("add")
    print(items)
    item_description = [item for item in items if str(item['dish_id']) == str(dish_id)]
    print(item_description)
    item_description = item_description[0]
    print(item_description)
    curr_basket = session.get('llist', {})


    curr_basket[dish_id] = {
                'dish_name': item_description['dish_name'],
                'dish_amount': item_description['dish_amount']
            }

    with DBContextManager(current_app.config['db_config']) as cursor:
        if cursor is None:
            raise ValueError('Курсор не создан')
        print("check_order_with_list key")
        for key in curr_basket:

            _sql3 = provider.get('edit_status.sql', status='type1', dish_id=key)
            print(key)
            cursor.execute(_sql3)

    session['llist'] = curr_basket
    session.permanent = False
    return True

@blueprint_verification.route('/save_order')
def check_order():
    global order_id
    global a
    current_basket = session.get('llist', {})
    print("checkorder current_basket")
    print(current_basket)

    #check_order_with_list(current_app.config['db_config'], current_basket)
    if current_basket:
        session.pop('llist')
    print(current_basket)
###############
    sql = provider.get('select_check_order_list.sql')
    result = select_dict(current_app.config['db_config'], sql)
    a=0
    order_id = 0
    if result:
        return redirect(url_for('bp_verification.verification'))
    else:
        return render_template('orders_checked.html')



def check_order_with_list(dbconfig: dict, current_basket: dict):
    with DBContextManager(dbconfig) as cursor:
        if cursor is None:
            raise ValueError('Курсор не создан')
        print("check_order_with_list key")
        for key in current_basket:
            _sql3 = provider.get('edit_status.sql', status='type1', dish_id=key)
            print(key)
            cursor.execute(_sql3)



@blueprint_verification.route('/clear-basket')
def clear_basket():
    if 'llist' in session:
        session.pop('llist')
    return redirect(url_for('bp_verification.verification'))