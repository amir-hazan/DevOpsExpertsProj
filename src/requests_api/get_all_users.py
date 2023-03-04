import os
import sys
import json

# define root source path
package_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.append(package_path)

import requests
from src.App.AppSettings import ApplicationSettings


class GetAllUsers:
    @staticmethod
    def get_all_users_from_db():
        """ GET request for getting username from db by user_id  """
        try:
            # get settings from App settings class
            get_app_settings_obj = ApplicationSettings

            url = get_app_settings_obj.get_rest_app_get_all_users_url()

            get_res = requests.get(url)

            if get_res.ok:
                json_output = json.dumps(get_res.json(), indent=2)
                print(json_output)
            else:
                response_err = {
                    'errorMessage': 'Unable to get all users',
                    'statusCode': get_res.status_code
                }
                print(response_err)

        except requests.exceptions.ConnectionError as reqExecConErr:
            print(reqExecConErr, "\n\nDoes rest_app.py is running?")
            sys.exit(1)


GetAllUsers.get_all_users_from_db()
