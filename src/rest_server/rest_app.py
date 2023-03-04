import os
import sys

# define root source path
package_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.append(package_path)

import pymysql
import platform
from flask import Flask, request, make_response, jsonify, send_file
from src.db.db_connector import DBConnector
from src.db.check_table_exist import CheckTableExist
from src.App.AppSettings import ApplicationSettings
from src.db.get_table import GetTablesFromDB
from src.admin.stop_flask_server import StopFlaskServer


""" Flask rest application, running on Port 5000 """

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False


@app.route('/', methods=['GET'])
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


@app.route('/users/<user_id>', methods=['GET', 'POST', 'DELETE', 'PUT'])
def user(user_id):
    if request.method == "POST":

        # getting the json data payload from request
        request_data = request.json
        # treating request_data as a dictionary to get a specific value from key
        user_name = request_data.get('user_name')
        # Set Date created
        date_created = get_app_settings_obj.get_date_time()

        obj_add_new_user = DBConnector(user_id, user_name, date_created, None)

        if obj_add_new_user.add_new_user() is False:
            response = make_response(
                jsonify(
                    {
                        "status": "Error",
                        "reason": "ID: " + user_id + " Already exist"
                    }
                )
            )

            response.headers['Content-Type'] = 'application/json'
            return response, 500

        response = make_response(
            jsonify(
                {
                    "status": "OK",
                    "user_id": int(user_id),
                    "user_name": user_name,
                    "date_created": str(date_created)
                }
            )
        )

        response.headers['Content-Type'] = 'application/json'
        return response, 200

    elif request.method == "GET":

        obj_get_user_name_by_id = DBConnector(user_id, None, None, None)
        get_method_result = obj_get_user_name_by_id.get_existing_user_by_id()

        if get_method_result is not None:
            user_name = get_method_result[0]
            date_created = str(get_method_result[1])
        else:
            user_name = None

        if not user_name and user_name is not False:
            response = make_response(
                jsonify(
                    {
                        "status": "Error",
                        "reason": "No such ID: " + user_id
                    }
                )
            )

            response.headers['Content-Type'] = 'application/json'
            return response, 404

        elif user_name is False:
            if platform.system() == 'Windows':
                win_err_html_url = package_path + '\\src\\html_files\\404_rest.html'
                return send_file(win_err_html_url), 404
            elif platform.system() == 'Darwin' or platform.system() == 'Linux':
                unix_err_html_url = package_path + '/src/html_files/404_rest.html'
                return send_file(unix_err_html_url), 404

        elif user_name is not None and user_name is not False:
            response = make_response(
                jsonify(
                    {
                        "status": "OK",
                        "user_id": int(user_id),
                        "user_name": user_name,
                        "date_created": date_created
                    }
                )
            )

            response.headers['Content-Type'] = 'application/json'
            return response, 200

    elif request.method == "PUT":

        # getting the json data payload from request
        request_data = request.json
        # treating request_data as a dictionary to get a specific value from key
        new_user_name = request_data.get('user_name')
        # Set Date created
        date_created = get_app_settings_obj.get_date_time()

        obj_update_user_name_by_id = DBConnector(user_id, None, date_created, new_user_name)

        if obj_update_user_name_by_id.update_existing_user_by_id() is False:
            response = make_response(
                jsonify(
                    {
                        "status": "Error",
                        "reason": "Cannot update to the same user name '" + new_user_name + "'"
                    }
                )
            )

            response.headers['Content-Type'] = 'application/json'
            return response, 403

        elif obj_update_user_name_by_id.update_existing_user_by_id() is None:
            response = make_response(
                jsonify(
                    {
                        "status": "Error",
                        "reason": "User ID '" + user_id + "' does not exist"
                    }
                )
            )

            response.headers['Content-Type'] = 'application/json'
            return response, 404

        elif obj_update_user_name_by_id.update_existing_user_by_id() == "Error":
            response = make_response(
                jsonify(
                    {
                        "status": "Error",
                        "reason": "wrong type of user_id: '" + user_id + "' must be int and without special chars"
                    }
                )
            )

            response.headers['Content-Type'] = 'application/json'
            return response, 403

        response = make_response(
            jsonify(
                {
                    "status": "OK",
                    "user_id": user_id,
                    "user_name": new_user_name,
                    "date_created": str(date_created)
                }
            )
        )

        response.headers['Content-Type'] = 'application/json'
        return response, 200

    elif request.method == "DELETE":

        obj_delete_user_by_id = DBConnector(user_id, None, None, None)

        if obj_delete_user_by_id.delete_existing_user_by_id() is False:
            response = make_response(
                jsonify(
                    {
                        "status": "Error",
                        "isDeleted": False,
                        "reason": "User ID '" + user_id + "' does not exist"
                    }
                )
            )

            response.headers['Content-Type'] = 'application/json'
            return response, 404

        elif obj_delete_user_by_id.delete_existing_user_by_id() == "Error":
            response = make_response(
                jsonify(
                    {
                        "status": "Error",
                        "reason": "wrong type of user_id: '" + user_id + "' must be int and without special chars"
                    }
                )
            )

            response.headers['Content-Type'] = 'application/json'
            return response, 403

        response = make_response(
            jsonify(
                {
                    "status": "OK",
                    "user_id": int(user_id),
                    "isDeleted": True
                }
            )
        )

        response.headers['Content-Type'] = 'application/json'
        return response, 200


@app.route('/users/add-new-user', methods=['POST', 'GET', 'PUT', 'DELETE'])
def auto_create_user():
    if request.method == "POST":

        # getting the json data payload from request
        request_data = request.json
        # treating request_data as a dictionary to get a specific value from key
        user_name = request_data.get('user_name')
        # Set Date created
        date_created = get_app_settings_obj.get_date_time()

        obj_create_user_with_auto_id = DBConnector(None, user_name, date_created, None)
        user_id = obj_create_user_with_auto_id.get_next_available_user_id_from_db()

        if obj_create_user_with_auto_id.create_user_based_on_available_id() is False:
            response = make_response(
                jsonify(
                    {
                        "status": "Error",
                        "reason": "Unknown Error"
                    }
                )
            )

            response.headers['Content-Type'] = 'application/json'
            return response, 500

        response = make_response(
            jsonify(
                {
                    "status": "OK",
                    "user_id": user_id,
                    "user_name": user_name,
                    "date_created": str(date_created)
                }
            )
        )

        response.headers['Content-Type'] = 'application/json'
        return response, 200

    else:
        response = make_response(
            jsonify(
                {
                    "status": "Error",
                    "reason": "Method '" + request.method + "' Not Allowed",
                    "Allowed Method": "POST"
                }
            )
        )
        response.headers['Content-Type'] = 'application/json'
        return response, 405


@app.route('/users/json/get-all-users', methods=['GET'])
def get_all_users():
    if request.method == "GET":

        if DBConnector.get_users_table_as_json() is False:
            response = make_response(
                jsonify(
                    {
                        "status": "Error",
                        "reason": "No users in db"
                    }
                )
            )

            response.headers['Content-Type'] = 'application/json'
            return response, 404

        res = DBConnector.get_users_table_as_json()
        response = make_response(res)
        response.headers['Content-Type'] = 'application/json'
        return response, 200


@app.route('/users/get-users-table', methods=['GET'])
def get_users_table():
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


@app.route('/admin/json/get-config-table', methods=['GET'])
def get_config_json():
    if request.method == "GET":

        if DBConnector.get_config_table_as_json() is False:
            response = make_response(
                jsonify(
                    {
                        "status": "Error",
                        "reason": "No data in config table"
                    }
                )
            )

            response.headers['Content-Type'] = 'application/json'
            return response, 404

        res = DBConnector.get_config_table_as_json()
        response = make_response(res)
        response.headers['Content-Type'] = 'application/json'
        return response, 200


@app.route('/admin/get-config-table', methods=['GET'])
def get_config_table():
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


@app.route('/admin/stop-rest-server', methods=['GET'])
def stop_rest_server():
    if request.method == 'GET':
        obj_stop_r_server = StopFlaskServer
        if obj_stop_r_server.stop_flask_rest_server() is True:
            response = make_response(
                jsonify(
                    {
                        "status": "rest server successfully stopped",
                        "is died": True
                    }
                )
            )

            response.headers['Content-Type'] = 'application/json'
            return response, 200


@app.errorhandler(404)
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
        app.run(host=get_app_settings_obj.get_flask_host_address_val(), debug=True, port=get_app_settings_obj.get_rest_app_server_port_val())
    else:
        print("Error, db tables is not exist")
except pymysql.err.ProgrammingError as err:
    print("rest server error:", err)
