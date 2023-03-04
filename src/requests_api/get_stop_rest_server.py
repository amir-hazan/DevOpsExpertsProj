import os
import sys

# define root source path
package_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.append(package_path)

import json
import requests
from src.App.AppSettings import ApplicationSettings


class SendGetReqStopRestServers:

    def __init__(self, get_response):
        self.get_response = get_response

    def send_get_req_stop_rest_server(self):

        get_response = self.get_response

        obj_build_stop_rest_server_url = ApplicationSettings
        url = obj_build_stop_rest_server_url.stop_server_rest_app_url()

        try:
            get_request = requests.get(url)
            if get_request.ok:
                res = {
                    'is stooped': True,
                    'server address': str(url),
                    'status code': get_request.status_code
                }

                get_response = json.dumps(res)
                print(get_response)

        except (Exception, requests.exceptions.ConnectionError) as e:
            if isinstance(e, requests.exceptions.ConnectionError):
                print(e, "\n\nDoes rest_app.py is running?")
                sys.exit(1)
            elif "ConnectionResetError" in str(e):
                print(get_response)
            else:
                print(e)
                sys.exit(1)


send_rest_stop_server_obj = SendGetReqStopRestServers(True)
send_rest_stop_server_obj.send_get_req_stop_rest_server()
