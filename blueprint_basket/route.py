import os
from datetime import datetime
from flask import Blueprint, render_template, request, current_app, session, redirect, url_for
from db_context_manager import DBContextManager
from access import group_required
from db_work import select_dict, insert
from sql_provider import SQLProvider

blueprint_order = Blueprint('bp_order', __name__, template_folder='templates', static_folder='static')

provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))

@blueprint_order.route('/', methods=['GET', 'POST'])
def order_index():
	db_config = current_app.config['db_config']
	if request.method == 'GET':
		sql = provider.get('all_items.sql')
		items = select_dict(db_config, sql)
		basket_items = session.get('basket', {})
		bill_dict = session.get('bill', {})

		return render_template('basket_order_list.html', items=items, basket=basket_items, bill=bill_dict)
	else:
		dish_id = request.form['dish_id']
		sql = provider.get('all_items.sql')
		items = select_dict(db_config, sql)

		add_to_basket(dish_id, items)

		return redirect(url_for('bp_order.order_index'))


def add_to_basket(dish_id: str, items:dict):
	item_description = [item for item in items if str(item['dish_id']) == str(dish_id)]
	item_description = item_description[0]
	curr_basket = session.get('basket', {})
	bill_dict = session.get('bill', {})

	if '1' in bill_dict:
		bill_dict['1']['bill'] += item_description['dish_price']
	else:
		bill_dict['1'] = {
			'bill': item_description['dish_price']
		}
		session['bill'] = bill_dict


	if dish_id in curr_basket:
		curr_basket[dish_id]['amount'] = curr_basket[dish_id]['amount'] + 1
	else:
		curr_basket[dish_id] = {
				'dish_name': item_description['dish_name'],
				'dish_price': item_description['dish_price'],
				'amount': 1
			}
		session['basket'] = curr_basket

		session.permanent = True

	return True


@blueprint_order.route('/save_order')
def save_order():
	user_id = session.get('user_id')
	current_basket = session.get('basket', {})
	bill_dict = session.get('bill', {})
	order_id = save_order_with_list(current_app.config['db_config'], user_id, current_basket, bill_dict)
	print(current_basket)
	if order_id:
		session.pop('basket')
		session.pop('bill')
		return render_template('order_created.html', order_id=order_id)
	else:
		return 'Что-то пошло не так'


def save_order_with_list(dbconfig: dict, user_id: int, current_basket: dict, bill_dict: dict):
	with DBContextManager(dbconfig) as cursor:
		if cursor is None:
			raise ValueError('Курсор не создан')

		order_date=datetime.now().date()

		_sql1 = provider.get('insert_order.sql', user_id=user_id, order_date='2022-07-07', bill=bill_dict['1']['bill'])#order_date
		print(_sql1)
		result1 = cursor.execute(_sql1)
		if result1 == 1:
			_sql2 = provider.get('select_order_list_id.sql', user_id=user_id)
			cursor.execute(_sql2)
			order_id = cursor.fetchall()[0][0]
			print('order_id=', order_id)
			if order_id:
				for key in current_basket:
					#if key>0:
					print(key, current_basket[key]['amount'])
					dish_amount = current_basket[key]['amount']
					_sql3 = provider.get('insert_order_list.sql', order_id=order_id, dish_id=key, dish_amount=dish_amount)
					cursor.execute(_sql3)

				return order_id


@blueprint_order.route('/clear-basket')
def clear_basket():
	if 'basket' in session:
		session.pop('basket')
	if 'bill' in session:
		session.pop('bill')
	return redirect(url_for('bp_order.order_index'))


