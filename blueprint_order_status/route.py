import os
from flask import Blueprint, render_template, request, current_app, session, redirect, url_for
from db_context_manager import DBContextManager
from access import group_required
from db_work import select_dict, insert, execute_
from sql_provider import SQLProvider
import array as arr

blueprint_order_st = Blueprint('bp_order_st', __name__, template_folder='templates', static_folder='static')

provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))


@blueprint_order_st.route('/',methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        user_id = session.get('user_id')
        sql = provider.get('select_user_order_list.sql', user_id=user_id)
        result = select_dict(current_app.config['db_config'], sql)
        if result:
            id = result[0]['order_id']
            id_ = result[0]['order_id']
            k = 0
            o = 1
            n = 0
            m = len(result)
            list_1 = [0] * m
            list_2 = [0] * m
            list_2[0] = o
            type1 = 0
            type3 = 0
            status = [0] * m
            print(m)
            for i in range(m):
                print(i)
                if id == id_:
                    n += 1
                    if i == (m - 1):
                        list_1[i] = n
                else:
                    o += 1
                    id = id_
                    k += 1
                    list_1[i - 1] = n
                    n = 1
                    list_2[i] = o
                    type1 = 0
                    type3 = 0
                    if i == (m - 1):
                        list_1[i] = 1

                if i < m - 1:
                    id_ = result[i + 1]['order_id']

                if result[i]['order_list_status'] == 'type1':
                    type1 += 1
                elif result[i]['order_list_status'] == 'type3':
                    type3 += 1

                if type1 > 0 and type3 == 0:
                    status[k] = 'Заказ принят'
                elif type1 == 0 and type3 > 0:
                    status[k] = 'Заказ не может быть осуществлен'
                else:
                    status[k] = 'Некоторые позиции заказа не могут быть осуществлены'


        else:
            result=0
            list_1=0
            list_2=0
            m=0
            status=0
        return render_template('status.html', result=result, list_1=list_1, list_2=list_2, m=m, status=status)


    else:
        order_id_to_delete = request.form.get('order_id_to_delete')
        order_id_to_save = request.form.get('order_id_to_save')
        order_id_is_done = request.form.get('order_id_is_done')

        if order_id_to_delete:
            sql_1 = provider.get('delete_order_from_order_list.sql', order_id=order_id_to_delete)  #
            sql_2 = provider.get('delete_order_from_user_order.sql', order_id=order_id_to_delete)  #
            with DBContextManager(current_app.config['db_config']) as cursor:
                if cursor is None:
                    raise ValueError('Курсор не создан')
                else:
                    cursor.execute(sql_1)
                    cursor.execute(sql_2)
        elif order_id_to_save:

            # sql_1 = provider.get('edit_status.sql', status='sent for ver', order_id=order_id_to_save)
            sql_1 = provider.get('delete_type3.sql', order_id=order_id_to_save)
            sql_2 = provider.get('count_bill.sql', order_id=order_id_to_save)
            #
            with DBContextManager(current_app.config['db_config']) as cursor:
                if cursor is None:
                    raise ValueError('Курсор не создан')
                else:
                    cursor.execute(sql_1)
            result = select_dict(current_app.config['db_config'], sql_2)
            sql_3 = provider.get('set_new_bill.sql', order_id=order_id_to_save, bill=result[0]['sum(dish_price)'])
            with DBContextManager(current_app.config['db_config']) as cursor:
                if cursor is None:
                    raise ValueError('Курсор не создан')
                else:
                    cursor.execute(sql_3)

        elif order_id_is_done:
            sql = provider.get('set_status_done.sql', order_id=order_id_is_done)
            with DBContextManager(current_app.config['db_config']) as cursor:
                if cursor is None:
                    raise ValueError('Курсор не создан')
                else:
                    cursor.execute(sql)

        return redirect(url_for('bp_order_st.index'))


#@blueprint_order_st.route('/save_status')
#def save_status():



