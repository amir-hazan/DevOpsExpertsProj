import argparse
import itertools
import os
import platform
import sys
import time
import pymysql
import requests
from pypika import Table, Query
import socket
from dotenv import load_dotenv
from urllib.parse import urlparse

# define root source path
package_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.append(package_path)

from src.App.AppSettings import ApplicationSettings


class MultiPlatformBackendTesting:
    """ this class will be used for backend testing in docker-compose && k8s cluster """

    def __init__(self,
                 post_user_id,
                 post_user_name,
                 get_user_id,
                 get_user_name,
                 db_user_id,
                 backend_test_user_id,
                 backend_test_user_name
                 ):

        self.post_user_id = post_user_id
        self.post_user_name = post_user_name
        self.get_user_id = get_user_id
        self.get_user_name = get_user_name
        self.db_user_id = db_user_id
        self.backend_test_user_id = backend_test_user_id
        self.backend_test_user_name = backend_test_user_name

    @staticmethod
    def get_args_testing_type_from_user():
        """ one file to be run with user args for testing type: docker or k8s"""
        try:
            parser = argparse.ArgumentParser(description="Pass backend testing args in script")
            parser.add_argument("-t", "--type", required=False, help='Backend testing type, remoteDB, Docker or K8S', default="remotedb")
            testing_args = parser.parse_args()
            test_type_args = testing_args.type

        except UnboundLocalError as unLocalErr:
            print(unLocalErr)

        finally:
            return test_type_args

    @staticmethod
    def get_testing_host_name():
        hostname = "localhost"
        return hostname

    @staticmethod
    def get_testing_port():
        object_gen_args = MultiPlatformBackendTesting.get_args_testing_type_from_user()
        object_get_data_from_app_settings = ApplicationSettings

        if object_gen_args.lower() == "remotedb":  # for remoteDB backend testing get port from config.json
            port = object_get_data_from_app_settings.set_config_db_table_field_rest_app_port_value()

        elif object_gen_args.lower() == "docker":  # for Docker backend testing get port from config.json
            port = object_get_data_from_app_settings.set_config_db_table_field_rest_app_port_value()

        elif object_gen_args.lower() == "k8s":  # for k8s backend testing get rest port from txt file

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
                # print(f"\nGenerating users for: {object_gen_args.lower()} will use port: {port}")

        else:
            print("\nError: Cannot define port for unknown, allowed args: remoteDB, Docker, K8S!\n")
            sys.exit(1)

        return port

    @staticmethod
    def get_testing_url():
        object_build_url = MultiPlatformBackendTesting
        url = f"http://{object_build_url.get_testing_host_name()}:" \
              f"{object_build_url.get_testing_port()}/" \
              f"users/"

        return url

    @staticmethod
    def get_sql_data_for_db_conn():
        """ get data from env file """

        try:
            object_gen_args = MultiPlatformBackendTesting.get_args_testing_type_from_user()
            object_get_data_from_config = ApplicationSettings

            if platform.system() == 'Windows':
                env_file_path = package_path + "\\.env"
            elif platform.system() == 'Darwin' or platform.system() == 'Linux':
                env_file_path = package_path + "/.env"

            load_dotenv(env_file_path)

            if object_gen_args.lower() == "remotedb":  # if remote db get port and hostname from config.json
                db_host_name = object_get_data_from_config.get_db_host()
                sql_port_num = object_get_data_from_config.get_db_port()
                sql_user_name = object_get_data_from_config.get_db_user_name()
                sql_user_password = object_get_data_from_config.get_db_user_pass()
                sql_schema = object_get_data_from_config.get_db_schema_name()

            elif object_gen_args.lower() == "docker" or object_gen_args.lower() == "k8s":
                db_host_name = "localhost"
                sql_user_name = os.getenv("MYSQL_USER")
                sql_user_password = os.getenv("MYSQL_PASSWORD")
                sql_schema = os.getenv("MYSQL_DATABASE")

                if object_gen_args.lower() == "docker":  # if docker get port number from txt file
                    sql_port_num = os.getenv("MYSQL_HOST_PORT")

                elif object_gen_args.lower() == "k8s":  # if k8s get sql port number from txt file

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
    def db_handling():
        db_port_num = int(MultiPlatformBackendTesting.get_sql_data_for_db_conn()[0])
        sql_user_name = MultiPlatformBackendTesting.get_sql_data_for_db_conn()[1]
        sql_user_password = MultiPlatformBackendTesting.get_sql_data_for_db_conn()[2]
        sql_db_schema = MultiPlatformBackendTesting.get_sql_data_for_db_conn()[3]
        db_host_name = MultiPlatformBackendTesting.get_sql_data_for_db_conn()[4]

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

        connector = MultiPlatformBackendTesting.db_handling()
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

    @staticmethod
    def get_testing_username_from_db():

        # get settings from App settings class
        get_app_settings_obj = ApplicationSettings

        connector = MultiPlatformBackendTesting.db_handling()
        if connector is not None:
            cursor, conn = connector
        else:
            print("Error: db_connector method is not properly returned.")

        # PyPika SELECT
        get_test_username_from_config_table = Query.from_(get_app_settings_obj.get_db_schema_pypika_format().config).\
            select('testing_user_name')

        get_test_username_from_config_table = get_test_username_from_config_table.get_sql()
        get_test_username_from_config_table = get_test_username_from_config_table.replace('"', '')

        try:
            cursor.execute(get_test_username_from_config_table)
            conn.commit()

            if cursor.rowcount == 0:
                print("Cannot find testing username in config table")
            else:
                testing_username = cursor.fetchone()
                testing_username = str(*testing_username)
                # print(testing_username)

        except UnboundLocalError as Err:
            print("DB Testing Error:", Err)
            return None

        finally:
            cursor.close()
            conn.close()

        return testing_username

    def post_req_backend_testing(self):

        user_id = self.post_user_id
        user_name = self.post_user_name

        try:
            object_get_testing_url = MultiPlatformBackendTesting
            url = object_get_testing_url.get_testing_url() + str(user_id)

            post_req = requests.post(
                url,
                json={
                    "user_name": user_name
                }
            )

            if post_req.ok:
                user_id = post_req.json()['user_id']
                user_name = post_req.json()['user_name']

                print("\n#1 POST Response:", post_req.json())

            else:
                post_response = post_req.json()
                reason = post_response['reason']
                print("Error: cannot post new request:", reason, "status code:", post_req.status_code)
                return None

        except requests.exceptions.ConnectionError as reqExecConErr:
            print(reqExecConErr, "\n\nDoes rest_app.py is running?")
            sys.exit(1)

        return user_id, user_name

    def get_req_backend_testing(self):
        user_id = self.get_user_id

        try:
            object_get_testing_url = MultiPlatformBackendTesting
            url = object_get_testing_url.get_testing_url() + str(user_id)

            send_get_request = requests.get(
                url,
                json={
                    "user_id": user_id
                }
            )

            if send_get_request.ok:
                get_response_user_id = send_get_request.json()['user_id']
                get_response_user_name = send_get_request.json()['user_name']

                print("#2 GET Response:", send_get_request.json())

            else:
                post_response = send_get_request.json()
                get_error_reason = post_response['reason']
                print("error: cannot post GET request", get_error_reason, "status code:", send_get_request.status_code)
                return None

        except requests.exceptions.ConnectionError as reqExecConErr:
            print(reqExecConErr, "\n\nDoes rest_app.py is running?")
            sys.exit(1)

        return get_response_user_id, get_response_user_name

    def docker_backend_testing_check_db(self):

        user_id = self.db_user_id
        connector = MultiPlatformBackendTesting.db_handling()
        if connector is not None:
            cursor, conn = connector
        else:
            print("Error: db_connector method is not properly returned.")

        get_app_settings_obj = ApplicationSettings

        # PyPika SELECT
        users = Table(get_app_settings_obj.get_users_db_table_name())
        get_user_from_db = Query.from_(get_app_settings_obj.get_db_schema_pypika_format().users).select('*').where(
            users.user_id == user_id)
        get_user_from_db = get_user_from_db.get_sql()
        get_user_from_db = get_user_from_db.replace('"', '')

        try:
            cursor.execute(get_user_from_db)
            conn.commit()

            check_stored_data = cursor.rowcount

            data_list = []

            if check_stored_data <= 1:
                for row in cursor:
                    data_list.append(row)

                user_id_in_db = row[0]
                user_name_in_db = row[1]
                user_date_created = str(row[2])

                new_data_list = [user_id_in_db, user_name_in_db, user_date_created]
                print("#3 Data From db:", new_data_list)

            else:
                return None

        except UnboundLocalError as Err:
            print("DB Testing Error:", Err)
            return None

        finally:
            cursor.close()
            conn.close()

        return check_stored_data, user_id_in_db, user_name_in_db

    def start_preform_testing(self):

        backend_test_user_id = self.backend_test_user_id
        backend_test_user_name = self.backend_test_user_name

        print("\n###########################")
        print("Starting Backend Testing...")
        print("###########################")

        # TEST #1 - Send POST request (response will be user_id and user_name as in request response)
        object_post_req = MultiPlatformBackendTesting(backend_test_user_id, backend_test_user_name, None, None, None, None, None)
        post_req_func = object_post_req.post_req_backend_testing()
        if post_req_func is not None:
            posted_user_id = post_req_func[0]
            posted_user_name = post_req_func[1]
        else:
            print('Test cannot start.')
            sys.exit(1)

        # TEST #2 Send GET request based on params below (response will be user_id and user_name as in request response)
        object_get_req = MultiPlatformBackendTesting(None, None, backend_test_user_id, None, None, None, None)
        get_req_func = object_get_req.get_req_backend_testing()
        if get_req_func is not None:
            get_user_id = get_req_func[0]
            get_user_name = get_req_func[1]
        else:
            print('Test cannot start.')
            sys.exit(1)

        # TEST #3 get user_id and user_name from database
        object_get_from_db = MultiPlatformBackendTesting(None, None, None, None, backend_test_user_id, None, None)
        get_from_db_func = object_get_from_db.docker_backend_testing_check_db()
        if get_from_db_func is not None:
            db_stored_data = get_from_db_func[0]
            db_user_id = get_from_db_func[1]
            db_user_name = get_from_db_func[2]
        else:
            print('Test cannot start.')
            sys.exit(1)

        # START TESTINGS:

        try:
            # TEST #1: Compare POST And Get Values are equal #
            if posted_user_id != get_user_id or posted_user_name != get_user_name:
                raise Exception("Error: Test #1 FAIL - "
                                "POST and GET usernames are different.")
            else:
                print("\nTest #1 (POST and GET): PASS\n"
                      "post_user_id", posted_user_id, "equal to get_user_id", get_user_id,
                      "\npost_user_name", posted_user_name, "equal to get_user_name", get_user_name, "\n")

            # TEST #2: Check if POST Request Was Stored IN DB #
            if db_stored_data == 0 and (posted_user_id != db_user_id and posted_user_name != db_user_name):
                raise Exception("Error: Test #2 FAIL - "
                                "either data not stored in DB:", db_stored_data,
                                "Or db_user_id from db", db_user_id, "is not equal to post_user_id", posted_user_id,
                                "Or db_user_name from db", db_user_name, "is not equal to post_user_name", posted_user_name)
            else:
                print("Test #2 (DB): PASS\n"
                      "POST data was stored sucssfully in database (rows count):", db_stored_data,
                      "\ndb_user_id", db_user_id, "equal to post_user_id", posted_user_id,
                      "\ndb_user_name", db_user_name, "equal to post_user_name", posted_user_name, "\n")

        except Exception as e:
            print(e)


backend_testing_user_id = MultiPlatformBackendTesting.get_available_user_id_from_db()  # auto-generate user id
backend_testing_user_name = MultiPlatformBackendTesting.get_testing_username_from_db()
object_start_testing = MultiPlatformBackendTesting(None, None, None, None, None, backend_testing_user_id, backend_testing_user_name)
object_start_testing.start_preform_testing()
