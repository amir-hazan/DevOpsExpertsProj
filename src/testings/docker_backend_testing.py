import os
import sys
import socket
import platform
from dotenv import load_dotenv
import requests

# define root source path
package_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.append(package_path)

from src.App.AppSettings import ApplicationSettings
from src.db.db_connector import DBConnector
from pypika import Table, Query


class DockerBackendTestings:
    """ Backend testings based on POST And MySql """

    def __init__(self,
                 post_user_id,
                 post_user_name,
                 get_user_id,
                 get_user_name,
                 db_user_id,
                 backend_testing_user_id,
                 backend_testing_user_name
                 ):

        self.post_user_id = post_user_id
        self.post_user_name = post_user_name
        self.get_user_id = get_user_id
        self.get_user_name = get_user_name
        self.db_user_id = db_user_id
        self.backend_testing_user_id = backend_testing_user_id
        self.backend_testing_user_name = backend_testing_user_name

    @staticmethod
    def get_python_container_hostname_from_env_file():
        """ get hostname from .env file """
        try:
            if platform.system() == 'Windows':
                env_file_path = package_path + "\\.env"
            elif platform.system() == 'Darwin' or platform.system() == 'Linux':
                env_file_path = package_path + "/.env"

            load_dotenv(env_file_path)

        except AttributeError as e:
            print("An AttributeError occurred:", e)
            return False

        except Exception as err:
            print("Exception:", err)
            return False

        finally:
            python_container_hostname = os.getenv("PYTHON_CONTAINER_HOSTNAME")

        return python_container_hostname

    @staticmethod
    def docker_backend_testings_url():
        try:
            if DockerBackendTestings.get_python_container_hostname_from_env_file() is not False:
                py_container_host_name = DockerBackendTestings.get_python_container_hostname_from_env_file()
                # print(py_container_host_name)

                back_end_testings_url_obj = ApplicationSettings
                url = f"{back_end_testings_url_obj.get_config_protocol_val()}://" \
                      f"{py_container_host_name}:" \
                      f"{str(back_end_testings_url_obj.get_rest_app_server_port_val())}/" \
                      f"{back_end_testings_url_obj.get_testings_server_users_endpoint_val()}/"
            else:
                raise Exception('.env file exist?')

        except IndexError as indexErr:
            print("Exception:", indexErr)

        return url

    def docker_post_backend_testings(self):
        """ Backend testings compare get / post and db result """

        user_id = self.post_user_id
        user_name = self.post_user_name

        try:
            obj_url = DockerBackendTestings.docker_backend_testings_url()
            url = obj_url + str(user_id)

            # post request
            post_request = requests.post(
                url,
                json={
                    "user_name": user_name.lower()
                }
            )

            if post_request.ok:
                user_id = post_request.json()['user_id']
                user_name = post_request.json()['user_name']

                print("\n#1 POST Response:", post_request.json())

            else:
                post_res_dict = post_request.json()
                print("error: cannot post new request", post_res_dict['reason'],
                      "status code:", post_request.status_code)

        except requests.exceptions.ConnectionError as reqExecConErr:
            print(reqExecConErr, "\n\nDoes rest_app.py is running?")
            sys.exit(1)

        return user_id, user_name

    def docker_backend_get_request(self):
        """ Sending backend GET Request """

        user_id = self.get_user_id

        try:

            obj_url = DockerBackendTestings.docker_backend_testings_url()
            url = obj_url + str(user_id)

            send_get_request = requests.get(
                url,
                json=
                {
                    'user_id': user_id
                }
            )

            if send_get_request.ok:
                get_response_user_id = send_get_request.json()['user_id']
                get_response_user_name = send_get_request.json()['user_name']

                print("#2 GET Response:", send_get_request.json())
            else:
                return None

        except requests.exceptions.ConnectionError as reqExecConErr:
            print("\nError: Does rest_app.py is running?\n", reqExecConErr)
            sys.exit(1)

        finally:
            return get_response_user_id, get_response_user_name

    def docker_backend_check_posted_data_in_db(self):

        """" Check if Posted data was Stored in DB """

        user_id = self.db_user_id

        # get settings from App settings class
        get_app_settings_obj = ApplicationSettings

        # 3 query database (sql) and check if user "John" is equal to user_id

        cursor, conn = get_app_settings_obj.connect_to_database()

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

                return check_stored_data, user_id_in_db, user_name_in_db

            else:
                return None

        except UnboundLocalError as Err:
            print("DB Error:", Err)
        finally:
            cursor.close()
            conn.close()

    def start_docker_backend_testings(self):
        """ Run actual testing """

        backend_testing_user_id = self.backend_testing_user_id
        backend_testing_user_name = self.backend_testing_user_name

        print("Docker Backend Testing Started...")

        try:
            # Send POST request (response will be user_id and user_name as in request response)
            obj_post_request = DockerBackendTestings(backend_testing_user_id, backend_testing_user_name, None, None, None, None, None)
            list_from_post_req = [obj_post_request.docker_post_backend_testings()]
            post_user_id = list_from_post_req[0][0]
            post_user_name = list_from_post_req[0][1]

            # Send GET request based on params below (response will be user_id and user_name as in request response)
            obj_get_request = DockerBackendTestings(None, None, backend_testing_user_id, None, None, None, None)
            list_from_get_res = [obj_get_request.docker_backend_get_request()]
            get_user_id = list_from_get_res[0][0]
            get_user_name = list_from_get_res[0][1]

            # get user_id and user_name from database
            obj_db_test = DockerBackendTestings(None, None, None, None, backend_testing_user_id, None, None)
            list_from_db = [obj_db_test.docker_backend_check_posted_data_in_db()]
            check_stored_data = list_from_db[0][0]
            db_user_id = list_from_db[0][1]
            db_user_name = list_from_db[0][2]

            print("\nTesting Results will be display in a moment...")

            # TEST #1: Compare POST And Get Values are equal #
            if post_user_id != get_user_id or post_user_name != get_user_name:
                raise Exception("Error: Test #1 FAIL - "
                                "POST and GET usernames are different.")
            else:
                print("\nTest #1 (POST and GET): PASS\n"
                      "post_user_id", post_user_id, "equal to get_user_id", get_user_id,
                      "\npost_user_name", post_user_name, "equal to get_user_name", get_user_name, "\n")

            # TEST #2: Check if POST Request Was Stored IN DB #
            if check_stored_data == 0 and (post_user_id != db_user_id and post_user_name != db_user_name):
                raise Exception("Error: Test #2 FAIL - "
                                "either data not stored in DB:", check_stored_data,
                                "Or db_user_id from db", db_user_id, "is not equal to post_user_id", post_user_id,
                                "Or db_user_name from db", db_user_name, "is not equal to post_user_name",
                                post_user_name)
            else:
                print("Test #2 (DB): PASS\n"
                      "POST data was stored sucssfully in database (rows count):", check_stored_data,
                      "\ndb_user_id", db_user_id, "equal to post_user_id", post_user_id,
                      "\ndb_user_name", db_user_name, "equal to post_user_name", post_user_name, "\n")

        except Exception as e:
            print("Error:", e)

    @staticmethod
    def check_flask_port(host, port):
        is_port_opened = False
        while is_port_opened is False:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(5)
                s.connect((host, port))
                s.close()
                is_port_opened = True

            except socket.error as connErr:
                # print("Connection Error:", connErr)
                is_port_opened = False

        return is_port_opened

    @staticmethod
    def run_docker_backend_testings():
        py_container_host_name = DockerBackendTestings.get_python_container_hostname_from_env_file()
        if DockerBackendTestings.check_flask_port(py_container_host_name, 5000):
            print("Flask Server port: 5000 is open and ready for connections...")

            # get settings from App settings class
            get_app_settings_obj = ApplicationSettings
            set_backend_testing_user_id = DBConnector.get_next_available_user_id_from_db()  # auto-generate user id
            set_backend_testing_user_name = get_app_settings_obj.get_testing_user_from_config_db_val()  # username from config table

            obj_backend_testings = DockerBackendTestings(None, None, None, None, None, set_backend_testing_user_id, set_backend_testing_user_name)
            obj_backend_testings.start_docker_backend_testings()

        else:
            print("Flask Server port: 5000 is closed...")


docker_be_testing_obj = DockerBackendTestings
docker_be_testing_obj.run_docker_backend_testings()
