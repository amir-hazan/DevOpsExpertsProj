import os
import sys

# define root source path
package_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.append(package_path)

import requests
import names
from src.App.AppSettings import ApplicationSettings
from src.db.db_connector import DBConnector
from src.db.get_table import GetTablesFromDB


class UpdateUserNameByID:
    def __init__(self, user_id):
        self.user_id = user_id

    def update_user(self):
        """ PUT request for updating username from db by user_id  """

        try:
            user_id = self.user_id
            user_name = names.get_first_name()

            # get settings from App settings class
            get_app_settings_obj = ApplicationSettings

            url = get_app_settings_obj.get_rest_app_users_url() + str(user_id)

            post_req = requests.put(
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
                    'errorMessage': 'unable to update user',
                    'statusCode': post_req.status_code,
                    'reason': post_req.reason
                }
                print(response_err)

        except requests.exceptions.ConnectionError as reqExecConErr:
            print(reqExecConErr, "\n\nDoes rest_app.py is running?")
            sys.exit(1)


# random user id based on existing ids in db
exist_random_user_id = DBConnector.get_random_exist_user_id()
obj_put_req_user_by_id = UpdateUserNameByID(exist_random_user_id)
obj_put_req_user_by_id.update_user()
