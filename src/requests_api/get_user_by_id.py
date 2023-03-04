import os
import sys

# define root source path
package_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.append(package_path)

import requests
from src.App.AppSettings import ApplicationSettings
from src.db.db_connector import DBConnector


class GetRequestUserByID:
    def __init__(self, user_id):
        self.user_id = user_id

    def get_user_by_user_id(self):
        """ GET request for getting username from db by user_id  """

        try:
            user_id = self.user_id

            # get settings from App settings class
            get_app_settings_obj = ApplicationSettings

            url = get_app_settings_obj.get_rest_app_users_url() + str(user_id)

            get_res = requests.get(
                url,
                json={
                    'user_id': user_id
                }
            )

            if get_res.ok:
                print(get_res.json())
            else:
                response_err = {
                    'user_id': user_id,
                    'errorMessage': 'No such id',
                    'statusCode': get_res.status_code
                }
                print(response_err)

        except requests.exceptions.ConnectionError as reqExecConErr:
            print(reqExecConErr, "\n\nDoes rest_app.py is running?")
            sys.exit(1)


# random user id based on existing ids in db
exist_random_user_id = DBConnector.get_random_exist_user_id()
obj_get_req_user_by_id = GetRequestUserByID(exist_random_user_id)
obj_get_req_user_by_id.get_user_by_user_id()
