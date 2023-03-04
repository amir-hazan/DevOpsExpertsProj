import os
import sys

# define root source path
package_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.append(package_path)

import requests
import argparse
import names
from src.db.get_table import GetTablesFromDB
from src.App.AppSettings import ApplicationSettings
from src.db.db_connector import DBConnector


class AutoCreateUserID:
    def __init__(self, user_name):
        self.user_name = user_name

    def create_new_user_auto_generate_id(self):
        """ POST request for creating new user -- id will be auto generated based on last available id in DB """
        try:
            user_name = self.user_name

            # get settings from App settings class
            get_app_settings_obj = ApplicationSettings

            url = get_app_settings_obj.get_rest_app_create_users_url()
            # print("THE URL IS:", url)

            post_req = requests.post(
                url,
                json={
                    "user_name": user_name.lower()
                }
            )

            if post_req.ok:
                print(post_req.json())
                # obj_print_users_tbl = GetTablesFromDB(False, True, False, False, False, False)
                # obj_print_users_tbl.get_users_table()
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
    def start_creating_user():
        # # option using sys.argv[].

        # # if args from user is smaller than 1 create 10 users.
        # if len(sys.argv) >= 2:
        #     number_of_users_to_create = sys.argv[1]
        # else:
        #     number_of_users_to_create = 10

        try:
            parser = argparse.ArgumentParser(description='int, number of users to create, if 0 - 10 will be created as default')
            parser.add_argument('-n', '--num_of_users', required=True, help='Number of users to create in db')
            number_of_users_to_create = parser.parse_args()

            number_of_users_to_create = int(number_of_users_to_create.num_of_users)
            # print(type(number_of_users_to_create))

            if number_of_users_to_create < 1:
                number_of_users_to_create = 10  # if user choose less than 1 - create 10 users

            obj_create_user_with_auto_id = DBConnector(None, None, None, None)
            start_from_min_user_id = obj_create_user_with_auto_id.get_next_available_user_id_from_db()
            max_users_to_create = int(start_from_min_user_id) + int(number_of_users_to_create)

            for new_user in range(start_from_min_user_id, max_users_to_create):
                random_user_name = names.get_first_name()
                obj_create_auto_uname_id = AutoCreateUserID(random_user_name)
                obj_create_auto_uname_id.create_new_user_auto_generate_id()

            obj_print_users_tbl = GetTablesFromDB(False, True, False, False, False, False)
            obj_print_users_tbl.get_users_table()

        except ValueError as valErr:
            print(valErr)


ob_start_create_users = AutoCreateUserID
ob_start_create_users.start_creating_user()
