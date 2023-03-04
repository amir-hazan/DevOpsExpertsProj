import os
import sys
import pymysql
from pypika import Schema, Table, Query
import json
import time
import platform
import socket


class ApplicationSettings:

    @staticmethod
    def get_app_path():
        """  define root source path """
        package_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
        sys.path.append(package_path)
        return package_path

    @staticmethod
    def open_config_file():
        get_app_path_obj = ApplicationSettings
        app_path = get_app_path_obj.get_app_path()

        try:
            if platform.system() == 'Windows':
                with open(app_path + '\\src\\Config\\Config.json', 'r') as config_file:
                    return json.load(config_file)
            elif platform.system() == 'Darwin' or platform.system() == 'Linux':
                with open(app_path + '/src/Config/Config.json', 'r') as config_file:
                    return json.load(config_file)

        except FileNotFoundError as fileNotFoundErr:
            print("Error:", fileNotFoundErr)

    # DB Connection Settings from JSON #

    @staticmethod
    def get_db_host():
        obj_call_config = ApplicationSettings
        return obj_call_config.open_config_file()['DevOpsExpertsProj']['generalDBConfiguration']['dbHost']

    @staticmethod
    def get_db_port():
        obj_call_config = ApplicationSettings
        return obj_call_config.open_config_file()['DevOpsExpertsProj']['generalDBConfiguration']['dbPort']

    @staticmethod
    def get_db_user_name():
        obj_call_config = ApplicationSettings
        return obj_call_config.open_config_file()['DevOpsExpertsProj']['generalDBConfiguration']['dbUserName']

    @staticmethod
    def get_db_user_pass():
        obj_call_config = ApplicationSettings
        return obj_call_config.open_config_file()['DevOpsExpertsProj']['generalDBConfiguration']['dbUserPassword']

    @staticmethod
    def get_db_schema_name():
        obj_call_config = ApplicationSettings
        return obj_call_config.open_config_file()['DevOpsExpertsProj']['generalDBConfiguration']['dbSchemaName']

    # Users Table Settings From JSON #

    @staticmethod
    def get_users_db_table_name():
        obj_call_config = ApplicationSettings
        return obj_call_config.open_config_file()['DevOpsExpertsProj']['usersTableDBConfiguration']['tableName']

    @staticmethod
    def get_users_tbl_user_id_field():
        obj_call_config = ApplicationSettings
        return obj_call_config.open_config_file()['DevOpsExpertsProj']['usersTableDBConfiguration']['userIdField']

    @staticmethod
    def get_users_tbl_user_name_field():
        obj_call_config = ApplicationSettings
        return obj_call_config.open_config_file()['DevOpsExpertsProj']['usersTableDBConfiguration']['userNameField']

    @staticmethod
    def get_users_tbl_creation_date_field():
        obj_call_config = ApplicationSettings
        return obj_call_config.open_config_file()['DevOpsExpertsProj']['usersTableDBConfiguration']['creationDateField']

    # Config table settings #

    @staticmethod
    def get_config_db_table_name():
        obj_call_config = ApplicationSettings
        return obj_call_config.open_config_file()['DevOpsExpertsProj']['configTableDBConfiguration']['configTableFieldsName']['tableName']

    @staticmethod
    def get_config_db_id_field_name():
        obj_call_config = ApplicationSettings
        return obj_call_config.open_config_file()['DevOpsExpertsProj']['configTableDBConfiguration']['configTableFieldsName']['idField']

    @staticmethod
    def get_config_db_protocol_field_name():
        obj_call_config = ApplicationSettings
        return obj_call_config.open_config_file()['DevOpsExpertsProj']['configTableDBConfiguration']['configTableFieldsName']['protocolField']

    @staticmethod
    def get_config_db_flask_host_field_name():
        obj_call_config = ApplicationSettings
        app_config_file = obj_call_config.open_config_file()
        return app_config_file['DevOpsExpertsProj']['configTableDBConfiguration']['configTableFieldsName']['flaskHostAddressField']

    @staticmethod
    def get_config_db_server_testing_host_field_name():
        obj_call_config = ApplicationSettings
        app_config_file = obj_call_config.open_config_file()
        return app_config_file['DevOpsExpertsProj']['configTableDBConfiguration']['configTableFieldsName']['serverTestingHostAddressField']

    @staticmethod
    def get_config_db_rest_app_port_field_name():
        obj_call_config = ApplicationSettings
        app_config_file = obj_call_config.open_config_file()
        return app_config_file['DevOpsExpertsProj']['configTableDBConfiguration']['configTableFieldsName']['restAppPortField']

    @staticmethod
    def get_config_db_web_app_port_field_name():
        obj_call_config = ApplicationSettings
        app_config_file = obj_call_config.open_config_file()
        return app_config_file['DevOpsExpertsProj']['configTableDBConfiguration']['configTableFieldsName']['webAppPortField']

    @staticmethod
    def get_config_db_users_endpoint_field_name():
        obj_call_config = ApplicationSettings
        app_config_file = obj_call_config.open_config_file()
        return app_config_file['DevOpsExpertsProj']['configTableDBConfiguration']['configTableFieldsName']['usersEndpointField']

    @staticmethod
    def get_config_db_get_user_data_endpoint_field_name():
        obj_call_config = ApplicationSettings
        app_config_file = obj_call_config.open_config_file()
        return app_config_file['DevOpsExpertsProj']['configTableDBConfiguration']['configTableFieldsName']['getUsersDataEndpointField']

    @staticmethod
    def get_config_db_create_users_endpoint_field_name():
        obj_call_config = ApplicationSettings
        app_config_file = obj_call_config.open_config_file()
        return app_config_file['DevOpsExpertsProj']['configTableDBConfiguration']['configTableFieldsName']['createUsersEndpointField']

    @staticmethod
    def get_config_db_get_all_users_endpoint_field_name():
        obj_call_config = ApplicationSettings
        app_config_file = obj_call_config.open_config_file()
        return app_config_file['DevOpsExpertsProj']['configTableDBConfiguration']['configTableFieldsName']['getAllUsersEndpointField']

    @staticmethod
    def get_config_db_stop_rest_server_endpoint_field_name():
        obj_call_config = ApplicationSettings
        app_config_file = obj_call_config.open_config_file()
        return app_config_file['DevOpsExpertsProj']['configTableDBConfiguration']['configTableFieldsName']['stopRestServerEndpointField']

    @staticmethod
    def get_config_db_stop_web_server_endpoint_field_name():
        obj_call_config = ApplicationSettings
        app_config_file = obj_call_config.open_config_file()
        return app_config_file['DevOpsExpertsProj']['configTableDBConfiguration']['configTableFieldsName']['stopWebServerEndpointField']

    @staticmethod
    def get_config_db_browser_field_name():
        obj_call_config = ApplicationSettings
        app_config_file = obj_call_config.open_config_file()
        return app_config_file['DevOpsExpertsProj']['configTableDBConfiguration']['configTableFieldsName']['testingBrowserField']

    @staticmethod
    def get_config_db_user_name_field_name():
        obj_call_config = ApplicationSettings
        app_config_file = obj_call_config.open_config_file()
        return app_config_file['DevOpsExpertsProj']['configTableDBConfiguration']['configTableFieldsName']['testingUserNameField']

    # SET Default Values For Config Table #

    @staticmethod
    def set_config_db_table_field_id_value():
        obj_call_config = ApplicationSettings
        app_config_file = obj_call_config.open_config_file()
        return app_config_file['DevOpsExpertsProj']['configTableDBConfiguration']['configTableFieldsValues']['id']

    @staticmethod
    def set_config_db_table_field_protocol_value():
        obj_call_config = ApplicationSettings
        app_config_file = obj_call_config.open_config_file()
        return app_config_file['DevOpsExpertsProj']['configTableDBConfiguration']['configTableFieldsValues']['protocol']

    @staticmethod
    def set_config_db_table_field_host_value():
        obj_call_config = ApplicationSettings
        app_config_file = obj_call_config.open_config_file()
        return app_config_file['DevOpsExpertsProj']['configTableDBConfiguration']['configTableFieldsValues']['flaskHostAddress']

    @staticmethod
    def set_config_db_table_field_server_testing_host_value():
        obj_call_config = ApplicationSettings
        app_config_file = obj_call_config.open_config_file()
        return app_config_file['DevOpsExpertsProj']['configTableDBConfiguration']['configTableFieldsValues']['serverTestingHostAddress']

    @staticmethod
    def set_config_db_table_field_rest_app_port_value():
        obj_call_config = ApplicationSettings
        app_config_file = obj_call_config.open_config_file()
        return app_config_file['DevOpsExpertsProj']['configTableDBConfiguration']['configTableFieldsValues']['restAppPort']

    @staticmethod
    def set_config_db_table_field_web_app_port_value():
        obj_call_config = ApplicationSettings
        app_config_file = obj_call_config.open_config_file()
        return app_config_file['DevOpsExpertsProj']['configTableDBConfiguration']['configTableFieldsValues']['webAppPort']

    @staticmethod
    def set_config_db_table_field_users_endpoint_value():
        obj_call_config = ApplicationSettings
        app_config_file = obj_call_config.open_config_file()
        return app_config_file['DevOpsExpertsProj']['configTableDBConfiguration']['configTableFieldsValues']['usersEndpoint']

    @staticmethod
    def set_config_db_table_field_get_users_data_endpoint_value():
        obj_call_config = ApplicationSettings
        app_config_file = obj_call_config.open_config_file()
        return app_config_file['DevOpsExpertsProj']['configTableDBConfiguration']['configTableFieldsValues']['getUsersDataEndpoint']

    @staticmethod
    def set_config_db_table_field_create_users_endpoint_value():
        obj_call_config = ApplicationSettings
        app_config_file = obj_call_config.open_config_file()
        return app_config_file['DevOpsExpertsProj']['configTableDBConfiguration']['configTableFieldsValues']['createUsersEndpoint']

    @staticmethod
    def set_config_db_table_field_get_all_users_endpoint_value():
        obj_call_config = ApplicationSettings
        app_config_file = obj_call_config.open_config_file()
        return app_config_file['DevOpsExpertsProj']['configTableDBConfiguration']['configTableFieldsValues']['getAllUsersEndpoint']

    @staticmethod
    def set_config_db_table_field_stop_rest_server_value():
        obj_call_config = ApplicationSettings
        app_config_file = obj_call_config.open_config_file()
        return app_config_file['DevOpsExpertsProj']['configTableDBConfiguration']['configTableFieldsValues']['stopRestServerEndpoint']

    @staticmethod
    def set_config_db_table_field_stop_web_server_value():
        obj_call_config = ApplicationSettings
        app_config_file = obj_call_config.open_config_file()
        return app_config_file['DevOpsExpertsProj']['configTableDBConfiguration']['configTableFieldsValues']['stopWebServerEndpoint']

    @staticmethod
    def set_config_db_table_field_browser_value():
        obj_call_config = ApplicationSettings
        app_config_file = obj_call_config.open_config_file()
        return app_config_file['DevOpsExpertsProj']['configTableDBConfiguration']['configTableFieldsValues']['testingBrowser']

    @staticmethod
    def set_config_db_table_field_user_name_value():
        obj_call_config = ApplicationSettings
        app_config_file = obj_call_config.open_config_file()
        return app_config_file['DevOpsExpertsProj']['configTableDBConfiguration']['configTableFieldsValues']['testingUserName']

    # GET data from config table
    @staticmethod
    def get_config_table_id_val():
        get_config_data_from_db_obj = ApplicationSettings
        return get_config_data_from_db_obj.get_configurations_from_db()[0]

    @staticmethod
    def get_config_protocol_val():
        get_config_data_from_db_obj = ApplicationSettings
        return get_config_data_from_db_obj.get_configurations_from_db()[1]

    @staticmethod
    def get_flask_host_address_val():
        get_config_data_from_db_obj = ApplicationSettings
        return get_config_data_from_db_obj.get_configurations_from_db()[2]

    @staticmethod
    def get_testing_host_val():
        get_config_data_from_db_obj = ApplicationSettings
        return get_config_data_from_db_obj.get_configurations_from_db()[3]

    @staticmethod
    def get_rest_app_server_port_val():
        get_config_data_from_db_obj = ApplicationSettings
        return get_config_data_from_db_obj.get_configurations_from_db()[4]

    @staticmethod
    def get_web_app_server_port_val():
        get_config_data_from_db_obj = ApplicationSettings
        return get_config_data_from_db_obj.get_configurations_from_db()[5]

    @staticmethod
    def get_testings_server_users_endpoint_val():
        get_config_data_from_db_obj = ApplicationSettings
        return get_config_data_from_db_obj.get_configurations_from_db()[6]

    @staticmethod
    def get_testings_server_get_user_data_endpoint_val():
        get_config_data_from_db_obj = ApplicationSettings
        return get_config_data_from_db_obj.get_configurations_from_db()[7]

    @staticmethod
    def get_testings_server_create_users_endpoint_val():
        get_config_data_from_db_obj = ApplicationSettings
        return get_config_data_from_db_obj.get_configurations_from_db()[8]

    @staticmethod
    def get_testings_server_get_all_users_endpoint_val():
        get_config_data_from_db_obj = ApplicationSettings
        return get_config_data_from_db_obj.get_configurations_from_db()[9]

    @staticmethod
    def get_stop_rest_server_endpoint_from_db_val():
        get_config_data_from_db_obj = ApplicationSettings
        return get_config_data_from_db_obj.get_configurations_from_db()[10]

    @staticmethod
    def get_stop_web_server_endpoint_from_db_val():
        get_config_data_from_db_obj = ApplicationSettings
        return get_config_data_from_db_obj.get_configurations_from_db()[11]

    @staticmethod
    def get_browser_type_from_config_db_val():
        get_config_data_from_db_obj = ApplicationSettings
        return get_config_data_from_db_obj.get_configurations_from_db()[12]

    @staticmethod
    def get_testing_user_from_config_db_val():
        get_config_data_from_db_obj = ApplicationSettings
        return get_config_data_from_db_obj.get_configurations_from_db()[13]

        # Build URLS

    @staticmethod
    def get_rest_app_users_url():  # port 5000
        build_rest_app_users_url_obj = ApplicationSettings
        return f"{build_rest_app_users_url_obj.get_config_protocol_val()}://" \
               f"{build_rest_app_users_url_obj.get_flask_host_address_val()}:" \
               f"{str(build_rest_app_users_url_obj.get_rest_app_server_port_val())}/" \
               f"{build_rest_app_users_url_obj.get_testings_server_users_endpoint_val()}/"

    @staticmethod
    def get_rest_app_create_users_url():  # API URL for auto creating user ID
        build_rest_app_create_users_url_obj = ApplicationSettings
        return f"{build_rest_app_create_users_url_obj.get_config_protocol_val()}://" \
               f"{build_rest_app_create_users_url_obj.get_flask_host_address_val()}:" \
               f"{str(build_rest_app_create_users_url_obj.get_rest_app_server_port_val())}/" \
               f"{build_rest_app_create_users_url_obj.get_testings_server_create_users_endpoint_val()}"

    @staticmethod
    def get_rest_app_get_all_users_url():  # API URL for getting all users - port 5000
        build_rest_app_get_all_users_url_obj = ApplicationSettings
        return f"{build_rest_app_get_all_users_url_obj.get_config_protocol_val()}://" \
               f"{build_rest_app_get_all_users_url_obj.get_flask_host_address_val()}:" \
               f"{str(build_rest_app_get_all_users_url_obj.get_rest_app_server_port_val())}/" \
               f"{build_rest_app_get_all_users_url_obj.get_testings_server_get_all_users_endpoint_val()}"

    @staticmethod
    def get_web_app_users_url():  # port 5001
        build_web_app_user_url_obj = ApplicationSettings
        return f"{build_web_app_user_url_obj.get_config_protocol_val()}://" \
               f"{build_web_app_user_url_obj.get_flask_host_address_val()}:" \
               f"{str(build_web_app_user_url_obj.get_web_app_server_port_val())}/" \
               f"{build_web_app_user_url_obj.get_testings_server_users_endpoint_val()}/"

    @staticmethod
    def stop_server_rest_app_url():
        build_rest_app_stop_server_url_obj = ApplicationSettings
        return f"{build_rest_app_stop_server_url_obj.get_config_protocol_val()}://" \
               f"{build_rest_app_stop_server_url_obj.get_flask_host_address_val()}:" \
               f"{str(build_rest_app_stop_server_url_obj.get_rest_app_server_port_val())}/" \
               f"{build_rest_app_stop_server_url_obj.get_stop_rest_server_endpoint_from_db_val()}"

    @staticmethod
    def stop_server_web_app_url():
        build_web_app_stop_server_url_obj = ApplicationSettings
        return f"{build_web_app_stop_server_url_obj.get_config_protocol_val()}://" \
               f"{build_web_app_stop_server_url_obj.get_flask_host_address_val()}:" \
               f"{str(build_web_app_stop_server_url_obj.get_web_app_server_port_val())}/" \
               f"{build_web_app_stop_server_url_obj.get_stop_web_server_endpoint_from_db_val()}"

        # Get Current data and time

    @staticmethod
    def get_date_time():
        dt_for_db = time.strftime('%Y-%m-%d %H:%M:%S')
        return dt_for_db

    # Socket
    @staticmethod
    def wait_for_db(host, port):
        while True:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.connect((host, port))
                return True
            except socket.error:
                time.sleep(1)

    # DB Connection Settings
    @staticmethod
    def connect_to_database():
        if ApplicationSettings.wait_for_db(ApplicationSettings.get_db_host(), 3306) is True:
            db_connection_obj = ApplicationSettings
            """ Establish connection to MySQL DB """
            try:
                conn = pymysql.connect(
                    host=db_connection_obj.get_db_host(),
                    port=db_connection_obj.get_db_port(),
                    user=db_connection_obj.get_db_user_name(),
                    passwd=db_connection_obj.get_db_user_pass(),
                    db=db_connection_obj.get_db_schema_name()
                )
            except pymysql.err.OperationalError as operationalErr:
                print(operationalErr)
            finally:
                # Getting a cursor from Database
                cursor = conn.cursor()
                return cursor, conn

    # extra - get server configuration from database
    @staticmethod
    def get_configurations_from_db():
        get_db_conn_obj = ApplicationSettings
        # Establishing connection to db
        cursor, conn = get_db_conn_obj.connect_to_database()

        # PyPika SELECT
        config = Table(get_db_conn_obj.get_config_db_table_name())
        get_db_config_table = Query.from_(get_db_conn_obj.get_db_schema_pypika_format().config).select('*').where(
            config.id == get_db_conn_obj.set_config_db_table_field_id_value())

        get_db_config_table = get_db_config_table.get_sql()
        get_db_config_table = get_db_config_table.replace('"', '')

        cursor.execute(get_db_config_table)
        conn.commit()

        config_list = []

        for row in cursor:
            config_list.append(row)

        # print(config_list)

        try:
            config_tuple = (row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12], row[13])
            # print(config_tuple)

        except UnboundLocalError as localError:
            print("Error:", localError)
            return None
        finally:
            cursor.close()
            conn.close()

        return config_tuple

    # Extra - PyPika Schema
    @staticmethod
    def get_db_schema_pypika_format():
        pypika_db_schema_obj = ApplicationSettings
        return Schema(pypika_db_schema_obj.get_db_schema_name())
