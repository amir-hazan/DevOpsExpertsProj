import os
import sys

# define root source path
package_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.append(package_path)

import requests
from src.db.get_table import GetTablesFromDB
from src.App.AppSettings import ApplicationSettings


class CreateNewUser:
    def __init__(self,
                 user_id,
                 user_name):
        self.user_id = user_id
        self.user_name = user_name

    def create_new_user(self):
        """ POST request for creating new user """
        try:
            user_id = self.user_id
            user_name = self.user_name

            # get settings from App settings class
            get_app_settings_obj = ApplicationSettings

            url = get_app_settings_obj.get_rest_app_users_url() + str(user_id)

            post_req = requests.post(
                url,
                json={
                    "user_name": user_name.lower()
                }
            )

            if post_req.ok:
                print(post_req.json())
                obj_print_users_tbl = GetTablesFromDB(False, True, False, False, False, False)
                obj_print_users_tbl.get_users_table()
            else:
                response_err = {
                    'user_id': user_id,
                    'user_name': user_name,
                    'errorMessage': 'unable to create user',
                    'statusCode': post_req.status_code,
                    'reason': post_req.reason
                }
                print(response_err)

        except requests.exceptions.ConnectionError as reqExecConErr:
            print(reqExecConErr, "\n\nDoes rest_app.py is running?")
            sys.exit(1)

    @staticmethod
    def ask_user_info():
        while True:
            try:
                ask_user_id = int(input("type user_id: "))
                break
            except ValueError as valErr:
                # print("Error:", valErr, "\n\n")
                print("ANSWER MUST BE NUMBER, TRY AGAIN\n")
                continue

        ask_user_name = input("type username: ")

        ob_post_new_user = CreateNewUser(ask_user_id, ask_user_name)
        ob_post_new_user.create_new_user()


obj_ask_user_info = CreateNewUser(None, None)
obj_ask_user_info.ask_user_info()

