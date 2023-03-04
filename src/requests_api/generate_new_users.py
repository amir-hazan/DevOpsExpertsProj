import itertools
import json
import os
import platform
import socket
import sys
import time
import pymysql
from dotenv import load_dotenv
from pypika import Table, Query
from urllib.parse import urlparse

# define root source path
package_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.append(package_path)

import requests
import argparse
import names
from src.App.AppSettings import ApplicationSettings


class GenerateNewUsers:
    def __init__(self, user_name):
        self.user_name = user_name

    @staticmethod
    def get_generate_users_script_args():

        try:
            parser = argparse.ArgumentParser(description="Generate users based on input args")
            parser.add_argument("-t", "--type", required=True, help='Script type: remoteDB, Docker or K8S', default="docker")
            parser.add_argument("-n", "--numOfUsers", required=True, help='Number of users to create', default="10")
            generate_args = parser.parse_args()
            script_type_arg = generate_args.type
            num_of_users = generate_args.numOfUsers

        except UnboundLocalError as unLocalErr:
            print(unLocalErr)

        finally:
            return str(script_type_arg), int(num_of_users)

    @staticmethod
    def get_rest_host_name():
        object_get_data_from_app_settings = ApplicationSettings
        hostname = object_get_data_from_app_settings.set_config_db_table_field_server_testing_host_value()
        return hostname

    @staticmethod
    def get_rest_server_port():
        object_gen_args = GenerateNewUsers.get_generate_users_script_args()
        object_get_data_from_app_settings = ApplicationSettings

        if object_gen_args[0].lower() == "remotedb":  # for remoteDB backend testing get port from config.json
            port = object_get_data_from_app_settings.set_config_db_table_field_rest_app_port_value()

        elif object_gen_args[0].lower() == "docker":  # for Docker backend testing get port from config.json
            port = object_get_data_from_app_settings.set_config_db_table_field_rest_app_port_value()

        elif object_gen_args[0].lower() == "k8s":  # for k8s backend testing get rest port from txt file

            try:
                if platform.system() == 'Windows':
                    flask_port_file = package_path + "\\k8s-flask-port.txt"
                elif platform.system() == 'Darwin' or platform.system() == 'Linux':
                    flask_port_file = package_path + "/k8s-flask-port.txt"

            except AttributeError as attErr:
                print("An AttributeError occurred:", attErr)

            except Exception as e:
                print("Exception:", e)

            finally:

                with open(flask_port_file, 'r') as f:  # , encoding='utf-16-le' - from local env
                    url = f.read()
                    url = ''.join(filter(str.isprintable, url)).strip()

                parsed_url = urlparse(url)
                port = str(parsed_url.port)
                # print(f"\nGenerating users for: {object_gen_args[0].lower()} will use port: {port}")

        else:
            print("\nError: Cannot define port for unknown, allowed args: remoteDB, Docker, K8S!\n")
            sys.exit(1)

        return port

    @staticmethod
    def get_sql_data_for_db_conn():
        """ get data from env file """

        try:
            object_gen_args = GenerateNewUsers.get_generate_users_script_args()
            object_get_data_from_config = ApplicationSettings

            if platform.system() == 'Windows':
                env_file_path = package_path + "\\.env"
            elif platform.system() == 'Darwin' or platform.system() == 'Linux':
                env_file_path = package_path + "/.env"

            load_dotenv(env_file_path)

            if object_gen_args[0].lower() == "remotedb":  # if remote db get port and hostname from config.json
                db_host_name = object_get_data_from_config.get_db_host()
                sql_port_num = object_get_data_from_config.get_db_port()
                sql_user_name = object_get_data_from_config.get_db_user_name()
                sql_user_password = object_get_data_from_config.get_db_user_pass()
                sql_schema = object_get_data_from_config.get_db_schema_name()

            elif object_gen_args[0].lower() == "docker" or object_gen_args[0].lower() == "k8s":
                db_host_name = "localhost"
                sql_user_name = os.getenv("MYSQL_USER")
                sql_user_password = os.getenv("MYSQL_PASSWORD")
                sql_schema = os.getenv("MYSQL_DATABASE")

                if object_gen_args[0].lower() == "docker":  # if docker get port number from txt file
                    sql_port_num = os.getenv("MYSQL_HOST_PORT")

                elif object_gen_args[0].lower() == "k8s":  # if k8s get sql port number from txt file

                    try:

                        if platform.system() == 'Windows':
                            mysql_port_file = package_path + "\\k8s-mysql-port.txt"
                        elif platform.system() == 'Darwin' or platform.system() == 'Linux':
                            mysql_port_file = package_path + "/k8s-mysql-port.txt"

                        with open(mysql_port_file, 'r') as f:  # , encoding='utf-16-le' - from local env
                            url = f.read()
                            url = ''.join(filter(str.isprintable, url)).strip()

                    except AttributeError as attErr:
                        print("AttributeError:", attErr)

                    except Exception as e:
                        print("Exception:", e)

                    finally:
                        parsed_url = urlparse(url)
                        sql_port_num = parsed_url.port

            else:
                print(f"wrong input value, must be 'remoteDB', 'Docker' or 'K8S'.")

        except AttributeError as e:
            print("An AttributeError occurred:", e)
            return False

        except Exception as err:
            print("Exception:", err)
            return False

        return sql_port_num, sql_user_name, sql_user_password, sql_schema, db_host_name

    @staticmethod
    def get_generate_request_url():
        object_request_settings = ApplicationSettings
        object_get_url = GenerateNewUsers
        protocol = object_request_settings.set_config_db_table_field_protocol_value()
        endpoint = object_request_settings.set_config_db_table_field_create_users_endpoint_value()
        url = f"{protocol}://{object_get_url.get_rest_host_name()}:" \
              f"{object_get_url.get_rest_server_port()}/{endpoint}"

        return url

    @staticmethod
    def db_handling():
        db_port_num = int(GenerateNewUsers.get_sql_data_for_db_conn()[0])
        sql_user_name = GenerateNewUsers.get_sql_data_for_db_conn()[1]
        sql_user_password = GenerateNewUsers.get_sql_data_for_db_conn()[2]
        sql_db_schema = GenerateNewUsers.get_sql_data_for_db_conn()[3]
        db_host_name = GenerateNewUsers.get_sql_data_for_db_conn()[4]

        def wait_for_db(host, port):
            while True:
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.connect((host, port))
                    return True
                except socket.error:
                    time.sleep(1)

        def db_connector():  # get values from config.json!!!
            if wait_for_db(db_host_name, db_port_num) is True:
                try:
                    conn = pymysql.Connect(
                        host=db_host_name,
                        port=db_port_num,
                        user=sql_user_name,
                        password=sql_user_password,
                        db=sql_db_schema
                    )

                except pymysql.err.OperationalError as operationalErr:
                    print(operationalErr)

                finally:
                    cursor = conn.cursor()
                    return cursor, conn

        return db_connector()

    @staticmethod
    def get_available_user_id_from_db():
        """ SQL Query that gets all next available id based on all id's in DB """

        # get settings from App settings class
        get_app_settings_obj = ApplicationSettings

        connector = GenerateNewUsers.db_handling()
        if connector is not None:
            cursor, conn = connector
        else:
            print("Error: db_connector method is not properly returned.")

        # PyPika SELECT
        users = Table(get_app_settings_obj.get_users_db_table_name())
        get_all_users_ids = Query.from_(get_app_settings_obj.get_db_schema_pypika_format().users).select(
            users.user_id
        )

        get_all_users_ids = get_all_users_ids.get_sql()
        get_all_users_ids = get_all_users_ids.replace('"', '')  # Removing apostrophes from relevant strings

        cursor.execute(get_all_users_ids)
        conn.commit()

        get_db_current_users_id = []

        # get all users id's from db into list
        for row in cursor:
            get_db_current_users_id.append(row)

        # clear list of user id's formatting
        get_db_current_users_id = list(itertools.chain(*get_db_current_users_id))
        # print("current list from db", get_db_current_users_id)

        try:
            # if db is empty set default user_id value to 1
            if not get_db_current_users_id:
                next_available_user_id = 1

            else:
                # find missing ids in 'get_db_current_users_id' based on db query result
                missing_id_nums_in_list = sorted(
                    set(range(1, get_db_current_users_id[-1])) - set(get_db_current_users_id))
                # print("missing numbers:", missing_id_nums_in_list)

                # if there is no missing numbers in 'missing_id_nums_in_list',
                # we'll add +1 to the largest number in 'get_db_current_users_id' (from db)
                if not missing_id_nums_in_list:
                    # print("no missing id's in list missing_id_nums_in_list:", missing_id_nums_in_list)
                    next_available_user_id = max(get_db_current_users_id) + 1
                    # print("new user id defined:", next_available_user_id)

                else:  # if there is missing numbers in list we'll use the lowest number from 'missing_id_nums_in_list'
                    next_available_user_id = min(missing_id_nums_in_list)
                    # print("### new user id:", next_available_user_id)

        except ValueError as val:
            print(val)
        except UnboundLocalError as localErr:
            print(localErr)
        finally:
            cursor.close()
            conn.close()

        return next_available_user_id

    def create_new_user_auto_generate_id(self):
        """ POST request for creating new user -- id will be auto generated based on last available id in DB """
        try:
            user_name = self.user_name

            # get settings from App settings class
            get_url_object = GenerateNewUsers
            url = get_url_object.get_generate_request_url()

            post_req = requests.post(
                url,
                json={
                    "user_name": user_name.lower()
                }
            )

            if post_req.ok:
                json_output = json.dumps(post_req.json(), indent=2)
                print(json_output)
            else:
                response_err = {
                    'user_name': user_name,
                    'errorMessage': 'unable to create user',
                    'statusCode': post_req.status_code,
                    'reason': post_req.reason
                }
                print(response_err)
                return

        except requests.exceptions.ConnectionError as reqExecConErr:
            print(reqExecConErr, "\n\nDoes rest_app.py is running?")
            sys.exit(1)

    @staticmethod
    def start_generating_users():

        object_get_num_of_users = GenerateNewUsers.get_generate_users_script_args()[1]

        # try:
        number_of_users_to_create = int(object_get_num_of_users)
        # print(type(number_of_users_to_create))

        if number_of_users_to_create < 1:
            number_of_users_to_create = 10  # if user choose less than 1 - create 10 users

        obj_create_user_with_auto_id = GenerateNewUsers.get_available_user_id_from_db()
        start_from_min_user_id = obj_create_user_with_auto_id
        max_users_to_create = int(start_from_min_user_id) + int(number_of_users_to_create)

        for new_user in range(start_from_min_user_id, max_users_to_create):
            random_user_name = names.get_first_name()
            obj_create_auto_uname_id = GenerateNewUsers(random_user_name)
            obj_create_auto_uname_id.create_new_user_auto_generate_id()

        # except ValueError as valErr:
        #     print("Error:", valErr)


object_run_generate_users = GenerateNewUsers
object_run_generate_users.start_generating_users()
