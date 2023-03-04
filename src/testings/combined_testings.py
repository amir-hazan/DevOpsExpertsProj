import os
import sys

# define root source path
package_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.append(package_path)

from src.db.db_connector import DBConnector
from src.App.AppSettings import ApplicationSettings
import requests
from pypika import Table, Query
from selenium import webdriver
import selenium.common.exceptions
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import platform


class CombinedTestingsActions:
    """ Combine test for backend and frontend class """
    def __init__(self,
                 post_user_id,
                 post_user_name,
                 get_user_id,
                 get_user_name,
                 db_user_id,
                 selenium_user_id,
                 testing_user_id,
                 testing_user_name
                 ):

        self.post_user_id = post_user_id
        self.post_user_name = post_user_name
        self.get_user_id = get_user_id
        self.get_user_name = get_user_name
        self.db_user_id = db_user_id
        self.selenium_user_id = selenium_user_id
        self.testing_user_id = testing_user_id
        self.testing_user_name = testing_user_name

    @staticmethod
    def get_request_url():
        """ Testings POST/GET Requests URL """

        # get settings from App settings class
        get_app_settings_obj = ApplicationSettings

        url = f"{get_app_settings_obj.get_config_protocol_val()}://" \
              f"{get_app_settings_obj.get_flask_host_address_val()}:" \
              f"{get_app_settings_obj.get_rest_app_server_port_val()}/" \
              f"{get_app_settings_obj.get_testings_server_users_endpoint_val()}/"

        return url

    def make_post_request(self):
        """ Sending POST request """

        user_id = self.post_user_id
        user_name = self.post_user_name

        try:
            # Get the Request URL
            obj_get_url = CombinedTestingsActions.get_request_url()
            url = obj_get_url + str(user_id)

            send_post_request = requests.post(
                url,
                json={
                    "user_name": user_name.lower()
                }
            )

            if send_post_request.ok:
                post_user_id = send_post_request.json()['user_id']
                post_username = send_post_request.json()['user_name']

                print("#1 POST Response:", send_post_request.json())

            else:
                post_res_dict = send_post_request.json()
                print(post_res_dict)
                return None

        except requests.exceptions.ConnectionError as reqExecConErr:
            print("\nError: Does rest_app.py is running?\n", reqExecConErr)
            sys.exit(1)

        finally:
            return post_user_id, post_username

    def make_get_request(self):
        """ Sending GET Request """

        user_id = self.get_user_id

        try:

            obj_get_url = CombinedTestingsActions.get_request_url()
            url = obj_get_url + str(user_id)

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

    def check_posted_data_in_db(self):
        """" Check if Posted data was Stored in DB """

        user_id = self.db_user_id

        # get settings from App settings class
        get_app_settings_obj = ApplicationSettings

        # 3 query database (sql) and check if user "John" is equal to user_id

        cursor, conn = get_app_settings_obj.connect_to_database()

        # PyPika SELECT
        users = Table(get_app_settings_obj.get_users_db_table_name())
        get_user_from_db = Query.from_(get_app_settings_obj.get_db_schema_pypika_format().users).select('*').where(users.user_id == user_id)
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

    def start_selenium_test(self):
        """" Selenium test for comparing selenium username with post username  """

        user_id = self.selenium_user_id

        # get settings from App settings class
        get_app_settings_obj = ApplicationSettings

        try:

            # use options to ignore ssl check
            options = webdriver.ChromeOptions()
            options.add_argument('--ignore-ssl-errors=yes')
            options.add_argument('--ignore-certificate-errors')

            # open & run web driver from specific location on disk
            if platform.system() == 'Windows':
                win_driver_path = package_path + "\\src\\web_driver\\chromedriver"
                driver = webdriver.Chrome(service=Service(win_driver_path), options=options)
            elif platform.system() == 'Darwin' or platform.system() == 'Linux':
                unix_driver_path = package_path + "/src/web_driver/chromedriver"
                driver = webdriver.Chrome(service=Service(unix_driver_path), options=options)

            # Build the URL from config table and user_id
            test_browser_url = f"{get_app_settings_obj.get_config_protocol_val()}://" \
                               f"{get_app_settings_obj.get_flask_host_address_val()}:" \
                               f"{get_app_settings_obj.get_web_app_server_port_val()}/" \
                               f"{get_app_settings_obj.get_testings_server_get_user_data_endpoint_val()}/" \
                               f"{user_id}"

            # open website on chrome using web driver
            driver.get(test_browser_url)

            # wait up tp 10 sec to website to load
            driver.implicitly_wait(10)

            user_name_from_web = driver.find_element(By.ID, value="uName").text

            if user_name_from_web:
                print("#4 Selenium response:", user_name_from_web)
                return user_name_from_web
            else:
                return None

        except selenium.common.exceptions.WebDriverException as webDriverErr:
            print("\nError: Does web_app.py is running?\n", webDriverErr)
        except Exception as exception:
            print(exception)
        finally:
            driver.close()

    def start_combined_testings(self):
        """ Run actual testing """

        testing_user_id = self.testing_user_id
        testing_user_name = self.testing_user_name

        print("Test Started...\n")

        try:
            # Send POST request (response will be user_id and user_name as in request response)
            obj_post_request = CombinedTestingsActions(testing_user_id, testing_user_name, None, None, None, None, None, None)
            list_from_post_req = [obj_post_request.make_post_request()]
            post_user_id = list_from_post_req[0][0]
            post_user_name = list_from_post_req[0][1]

            # Send GET request based on params below (response will be user_id and user_name as in request response)
            obj_get_request = CombinedTestingsActions(None, None, testing_user_id, None, None, None, None, None)
            list_from_get_res = [obj_get_request.make_get_request()]
            get_user_id = list_from_get_res[0][0]
            get_user_name = list_from_get_res[0][1]

            # get user_id and user_name from database
            obj_db_test = CombinedTestingsActions(None, None, None, None, testing_user_id, None, None, None)
            list_from_db = [obj_db_test.check_posted_data_in_db()]
            check_stored_data = list_from_db[0][0]
            db_user_id = list_from_db[0][1]
            db_user_name = list_from_db[0][2]

            # get selenium web test username
            obj_selenium_test = CombinedTestingsActions(None, None, None, None, None, testing_user_id, None, None)
            selenium_user_name = obj_selenium_test.start_selenium_test()

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

            # TEST #3: Open selenium and check that post_user_name is equal to selenium
            if post_user_name != selenium_user_name:
                raise Exception("Error: Test #3 FAIL - "
                                "post_user_name", post_user_name,
                                "is not equal to selenium_user_name", selenium_user_name)
            else:
                print("Test #3 (Selenium): PASS\n"
                      "post_user_name", post_user_name, "is equal to selenium_user_name", selenium_user_name)

        except Exception as e:
            print("Error:", e)


# get settings from App settings class
get_app_settings_obj = ApplicationSettings
set_testing_user_id = DBConnector.get_next_available_user_id_from_db()  # auto-generate user id
set_testing_user_name = get_app_settings_obj.get_testing_user_from_config_db_val()  # username from config table

obj_run_test = CombinedTestingsActions(None, None, None, None, None, None, set_testing_user_id, set_testing_user_name)
obj_run_test.start_combined_testings()
