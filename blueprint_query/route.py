import os

from flask import Blueprint, request, render_template, current_app
from db_work import select
from sql_provider import SQLProvider
from access import group_required

blueprint_query = Blueprint('bp_query', __name__, template_folder='templates')
#bp_query - имя blueprint которое фудет суффиксом ко всем именам методов данного модуля
#__name__ - имя исполняемого модуля относительно которого будет искаться папка blueprint_query и соответсвующие подкаталоги


provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))

@blueprint_query.route('/menu_query')
@group_required
def menu_query():
    return render_template('menu_query.html')

@blueprint_query.route('/task1', methods=['GET', 'POST'])
@group_required
def task1():
    if request.method == 'GET':
        return render_template('sum_cost_form.html')
    else:
            input_year = request.form.get('input_year')
            if input_year:
                _sql = provider.get('sum_cost_for_year.sql', input_year=input_year)
                year_result, schema = select(current_app.config['db_config'], _sql)
                if not year_result:
                    return render_template('sum_cost_form.html', error_message="Данных не найдено")
                else:
                    list_name = ['Сумма']
                    return render_template('sum_cost_for_years_result.html', schema=list_name, result=year_result, year=input_year)
            else:
                return render_template('sum_cost_form.html', error_message="Введите данные")


@blueprint_query.route('/task3', methods=['GET', 'POST'])
@group_required
def task3():
    if request.method == 'GET':
        return render_template('most_popular_dish_form.html')
    else:
            input_year = request.form.get('input_year')
            input_month = request.form.get('input_month')
            if input_year and input_month:
                _sql = provider.get('most_popular_dish.sql', input_year=input_year, input_month=input_month )
                info_result, schema = select(current_app.config['db_config'], _sql)
                if not info_result:
                    return render_template('most_popular_dish_form.html', error_message="Данных не найдено")
                else:
                    schema_=['Название', 'Количество', 'Выручка']
                    return render_template('most_popular_dish_result.html', schema=schema_, result=info_result, month=input_month, year=input_year) #, input_month=input_month, input_year=input_year
            else:
                return render_template('most_popular_dish_form.html', error_message="Введите данные")