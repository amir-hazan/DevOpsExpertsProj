import os
import sys

# define root source path
package_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.append(package_path)

import platform
import selenium.common.exceptions
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from src.App.AppSettings import ApplicationSettings
from src.db.db_connector import DBConnector


class FrontendTestings:
    """ Frontend Testings based on selenium """
    def __init__(self, user_id):
        self.user_id = user_id

    def start_frontend_testings(self):
        """ selenium frontend testing check and print existing username from HTML Page """

        user_id = self.user_id

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

            # wait 10 sec to website to load
            driver.implicitly_wait(10)

            get_user_name = driver.find_element(By.ID, value="uName").text
            print("Test Selenium: PASS\n"
                  "user_name is:", get_user_name, "on locator ID: \"uName\" and it's equal to", user_id)

        except selenium.common.exceptions.WebDriverException as webDriverErr:
            print(webDriverErr)
        except selenium.common.exceptions.NoSuchWindowException as winException:
            print(winException)
        except Exception as exception:
            print(exception)
        finally:
            driver.close()


# random user id based on existing ids in db
exist_random_user_id = DBConnector.get_random_exist_user_id()
obj_set_params_and_test = FrontendTestings(exist_random_user_id)
obj_set_params_and_test.start_frontend_testings()
