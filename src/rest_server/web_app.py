import os
import sys


# define root source path
package_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.append(package_path)

import pymysql
import platform
from flask import Flask, request, send_file, make_response, jsonify
from src.db.db_connector import DBConnector
from src.App.AppSettings import ApplicationSettings
from src.db.get_table import GetTablesFromDB
from src.admin.stop_flask_server import StopFlaskServer
from src.db.check_table_exist import CheckTableExist

""" Flask web application, running on Port 5001 """

web_app = Flask(__name__)
web_app.config['JSON_SORT_KEYS'] = False


@web_app.route('/', methods=['GET'])
def index_page():
    if request.method == 'GET':
        try:
            if platform.system() == 'Windows':
                win_users_tbl_html_url = package_path + '\\src\\html_files\\index.html'
                return send_file(win_users_tbl_html_url), 200
            elif platform.system() == 'Darwin' or platform.system() == 'Linux':
                unix_users_tbl_html_url = package_path + '/src/html_files/index.html'
                return send_file(unix_users_tbl_html_url), 200
        except FileNotFoundError as fileNotFoundErr:
            print("Error:", fileNotFoundErr)


@web_app.route('/users/get-user-data/<user_id>', methods=['GET'])
def get_users_name(user_id):
    if request.method == "GET":

        obj_get_username_by_id = DBConnector(user_id, None, None, None)
        get_method_result = obj_get_username_by_id.get_existing_user_by_id()

        if get_method_result is not None:
            user_name = get_method_result[0]
        else:
            user_name = None

        if user_name is False:
            if platform.system() == 'Windows':
                win_err_html_url = package_path + '\\src\\html_files\\404.html'
                return send_file(win_err_html_url), 404
            elif platform.system() == 'Darwin' or platform.system() == 'Linux':
                unix_err_html_url = package_path + '/src/html_files/404.html'
                return send_file(unix_err_html_url), 404

        elif not user_name and user_name is not False:
            return f"<p id='userNameErr' style='font-size: 40px'><b> No such ID</b></p>", 404
        else:
            return f"<p id='userName' style='font-size: 40px'><b>Hello <span style='color:red' id='uName'>{user_name}</span></b></p>", 200


@web_app.route('/users/get-users-table', methods=['GET'])
def get_all_users():
    if request.method == "GET":

        obj_get_all_users_table = GetTablesFromDB(False, False, True, False, False, False)
        obj_get_all_users_table.get_users_table()

        if DBConnector.get_users_table_as_json() is False:
            return f"<p id='error' style='font-size: 40px'><b>No users in DB</b></p>", 500

        try:
            if platform.system() == 'Windows':
                win_users_tbl_html_url = package_path + '\\src\\html_files\\users_table.html'
                return send_file(win_users_tbl_html_url), 200
            elif platform.system() == 'Darwin' or platform.system() == 'Linux':
                unix_users_tbl_html_url = package_path + '/src/html_files/users_table.html'
                return send_file(unix_users_tbl_html_url), 200
        except FileNotFoundError as fileNotFoundErr:
            print("Error:", fileNotFoundErr)


@web_app.route('/admin/get-config-table', methods=['GET'])
def get_config_tbl():
    if request.method == "GET":

        obj_save_config_table = GetTablesFromDB(False, False, False, False, False, True)
        obj_save_config_table.get_config_table()

        if DBConnector.get_config_table_as_json() is False:
            return f"<p id='error' style='font-size: 40px'><b> No data in DB</b></p>", 404

        try:
            if platform.system() == 'Windows':
                win_config_tbl_html_url = package_path + '\\src\\html_files\\config_table.html'
                return send_file(win_config_tbl_html_url), 200
            elif platform.system() == 'Darwin' or platform.system() == 'Linux':
                unix_config_tbl_html_url = package_path + '/src/html_files/config_table.html'
                return send_file(unix_config_tbl_html_url), 200
        except FileNotFoundError as fileNotFoundErr:
            print("Error:", fileNotFoundErr)


@web_app.route('/admin/stop-web-server', methods=['GET'])
def stop_web_server():
    if request.method == 'GET':
        obj_stop_r_server = StopFlaskServer
        if obj_stop_r_server.stop_flask_web_server() is True:
            response = make_response(
                jsonify(
                    {
                        "status": "web server successfully stopped",
                        "is died": True
                    }
                )
            )

            response.headers['Content-Type'] = 'application/json'
            return response, 200


@web_app.errorhandler(404)
def page_not_found(e):
    # 404 error when endpoint is invalid
    if platform.system() == 'Windows':
        win_err_html_url = package_path + '\\src\\html_files\\404.html'
        return send_file(win_err_html_url), 404
    elif platform.system() == 'Darwin' or platform.system() == 'Linux':
        unix_err_html_url = package_path + '/src/html_files/404.html'
        return send_file(unix_err_html_url), 404


try:
    check_db_tables_exist_result = CheckTableExist.check_if_tables_exist()
    if check_db_tables_exist_result is not False:
        get_app_settings_obj = ApplicationSettings
        web_app.run(host=get_app_settings_obj.get_flask_host_address_val(), debug=True, port=get_app_settings_obj.get_web_app_server_port_val())
    else:
        print("Error, db tables is not exist")
except pymysql.err.ProgrammingError as err:
    print("web server error:", err)
