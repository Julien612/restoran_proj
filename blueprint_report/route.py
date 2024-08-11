import os

from flask import Blueprint, request, render_template, current_app
from db_work import select, insert, call_proc, select_dict
from sql_provider import SQLProvider
from access import group_required
from db_context_manager import *

blueprint_report = Blueprint('bp_report', __name__, template_folder='templates')

provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))

@blueprint_report.route('/menu_report')
@group_required
def menu_report():
    return render_template('menu_report.html')

@blueprint_report.route('/view_report_1', methods=['GET', 'POST'])
@group_required
def view_report_1():
    if request.method == 'GET':
        return render_template('report_1_form.html')
    else:
        input_year = request.form.get('input_year')
        input_month = request.form.get('input_month')

        if input_year and input_month:
            sql = provider.get('check_if_exist.sql', input_year=input_year, input_month=input_month)
            result_, schema = select(current_app.config['db_config'], sql)
            if not result_:
                return render_template('report_1_form.html', error_message="Отчет на этот период еще не был создан")
            else:
                list=['Название', 'Проданное количество', 'Выручка']
                return render_template('report_1_result.html', schema=list, result=result_, month=input_month, year=input_year, rep1=1, rep2=0)
        else:
            return render_template('report_1_form.html', error_message="Введите данные")

@blueprint_report.route('/create_report_1', methods=['GET', 'POST'])
@group_required
def create_report_1():
    if request.method == 'GET':
        return render_template('report_1_form.html')
    else:
        input_year = request.form.get('input_year')
        input_month = request.form.get('input_month')

        if input_year and input_month:
            sql = provider.get('check_if_exist.sql', input_year=input_year, input_month=input_month)
            result_ = select_dict(current_app.config['db_config'], sql)

            if not result_:
                call_proc(current_app.config['db_config'], 'dish_report', input_month, input_year)
                return render_template('report_created.html')
            else:
                return render_template('report_1_form.html', error_message="Отчет на этот период уже был создан")
        else:
            return render_template('report_1_form.html', error_message="Введите данные")


#@blueprint_report.route('/create_report_2')
#@group_required
#def create_report_2():
#    rep_month=9
#    rep_year=2022
#    call_proc(current_app.config['db_config'], 'dish_report', rep_month, rep_year)
#    return render_template('report_created.html')


@blueprint_report.route('/view_report_2', methods=['GET', 'POST'])
@group_required
def view_report_2():
    if request.method == 'GET':
        return render_template('report_1_form.html')
    else:
        input_year = request.form.get('input_year')
        input_month = request.form.get('input_month')

        if input_year and input_month:
            sql = provider.get('check_if_exist_2.sql', input_year=input_year, input_month=input_month)
            result_, schema = select(current_app.config['db_config'], sql)
            if not result_:
                return render_template('report_1_form.html', error_message="Отчет на этот период еще не был создан")
            else:
                list=['Название', 'Количество', 'Месяц', 'Год']
                return render_template('report_1_result.html', schema=list, result=result_, month=input_month, year=input_year, rep1=0, rep2=1)
        else:
            return render_template('report_1_form.html', error_message="Введите данные")

@blueprint_report.route('/create_report_2', methods=['GET', 'POST'])
@group_required
def create_report_2():
    if request.method == 'GET':
        return render_template('report_1_form.html')
    else:
        input_year = request.form.get('input_year')
        input_month = request.form.get('input_month')

        if input_year and input_month:
            sql = provider.get('check_if_exist_2.sql', input_year=input_year, input_month=input_month)
            result_ = select_dict(current_app.config['db_config'], sql)

            if not result_:
                call_proc(current_app.config['db_config'], 'proc2', input_month, input_year)
                return render_template('report_created.html')
            else:
                return render_template('report_1_form.html', error_message="Отчет на этот период уже был создан")
        else:
            return render_template('report_1_form.html', error_message="Введите данные")


#@blueprint_report.route('/view_report_2', methods=['GET', 'POST'])
#@group_required
#def view_report_2():
#    _sql = provider.get('report_2_view.sql')
#    info_result, schema = select(current_app.config['db_config'], _sql)
#    return render_template('report_2_result.html', schema=schema, result=info_result)


#@blueprint_report.route('/create_report_2', methods=['GET', 'POST'])
#@group_required
#def create_report_2():
#    if request.method == 'GET':
#        return render_template('report_2_form.html')
#    else:
#        input_name = request.form.get('input_name')
#        input_col = request.form.get('input_col')
#        input_date = request.form.get('input_date')

#        if input_name and input_date and input_col:
#            _sql_ = provider.get('find_id_by_name.sql', input_name=input_name)
#            result_ = select_dict(current_app.config['db_config'], _sql_)

#            if not result_:
#                return render_template('report_2_form.html', error_message="Данные введены неверно")
#            else:
#                input_prod_id=result_[0]['prod_id']
#                _sql = provider.get('report_2_insert.sql', input_prod_id=input_prod_id, input_col=input_col,
#                                    input_date=input_date)
#                result=insert(current_app.config['db_config'], _sql)
#                if not result:
#                    return render_template('report_2_form.html', error_message="Данные введены неверно")
#                else:
#                    return render_template('report_2_form.html', error_message="Отчет успешно создан")
#        else:
#            return render_template('report_2_form.html', error_message="Введите данные")



