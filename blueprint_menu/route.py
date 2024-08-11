import os

from flask import Blueprint, render_template, request, current_app, session, redirect, url_for
from db_context_manager import DBContextManager
from access import group_required
from db_work import select_dict, insert
from sql_provider import SQLProvider

blueprint_menu = Blueprint('bp_menu', __name__, template_folder='templates', static_folder='static')

provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))


@blueprint_menu.route('/', methods=['GET', 'POST'])
@group_required
def menu():
    db_config = current_app.config['db_config']
    if request.method == 'GET':

        _sql1 = provider.get('select_menu.sql', status='type1')
        items = select_dict(db_config, _sql1)

        basket_items = session.get('llist', {})

        _sql2 = provider.get('select_menu.sql', status='type3')
        items2 = select_dict(db_config, _sql2)
        print(items, items2)
        print(len(items2))
        for i in range(len(items2)):
            dish_id=items2[i]['dish_id']
            print(dish_id)
            basket_items[dish_id] = {
                'dish_name': items2[i]['dish_name'],
            }
        print(basket_items)

        return render_template('menu_editting.html', items=items, list=basket_items)

    else:

        dish_id1 = request.form.get('dish_id_1')
        print("dish-id")
        print(dish_id1)
        dish_id2 = request.form.get('dish_id_2')
        print(dish_id2)
        _sql = provider.get('select_all_menu.sql')

        with DBContextManager(db_config) as cursor:
            if cursor is None:
                raise ValueError('Cursor not found')
            cursor.execute(_sql)
            result = []  # список, каждый элемент которого является словарем
            schema = [column[0] for column in cursor.description]
            for row in cursor.fetchall():
                result.append(dict(zip(schema, row)))

        items = result
        if dish_id1:
            add_to_list(dish_id1, items)
        elif dish_id2:
            add_to_list(dish_id2, items)

        return redirect(url_for('bp_menu.menu'))

def add_to_list(dish_id: str, items:dict):
    print("add")
    print(items, dish_id)
    item_description = [item for item in items if str(item['dish_id']) == str(dish_id)]
    print(item_description)
    item_description = item_description[0]
    print(item_description)
    curr_basket = session.get('llist', {})

    dish_status=item_description['dish_status']
    print(dish_status)
    with DBContextManager(current_app.config['db_config']) as cursor:
        if cursor is None:
            raise ValueError('Курсор не создан')

        if dish_status == 'type1':
            status='type3'
        else:
            status='type1'
        print(dish_id, status)
        _sql3 = provider.get('edit_status.sql', status=status, dish_id=dish_id)

        cursor.execute(_sql3)

    session['llist'] = curr_basket
    session.permanent = False
    return True


