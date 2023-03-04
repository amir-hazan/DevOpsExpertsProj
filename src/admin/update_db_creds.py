import sys
import os

# define root source path
package_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.append(package_path)

import json
import platform
import argparse


class UpdateDBCreds:

    """
    updating db configuration from cmd line:
    py update_db_creds.py db host, db port, username, password, schema
    """

    def __init__(self,
                 db_host_address,
                 db_username,
                 db_user_password,
                 config_table_host):

        self.db_host_address = db_host_address
        self.db_username = db_username
        self.db_user_password = db_user_password
        self.config_table_host = config_table_host

    def update_json_with_db(self):

        db_host_address = self.db_host_address
        db_username = self.db_username
        db_user_password = self.db_user_password
        config_table_host = self.config_table_host

        try:
            if platform.system() == 'Windows':
                config_path = package_path + '\\src\\Config\\Config.json'
            elif platform.system() == 'Darwin' or platform.system() == 'Linux':
                config_path = package_path + '/src/Config/Config.json'

            json_address = str(config_path)
            with open(json_address, 'r') as json_file:
                data = json.load(json_file)

                data['DevOpsExpertsProj']['generalDBConfiguration']['dbHost'] = db_host_address
                data['DevOpsExpertsProj']['generalDBConfiguration']['dbUserName'] = db_username
                data['DevOpsExpertsProj']['generalDBConfiguration']['dbUserPassword'] = db_user_password
                data['DevOpsExpertsProj']['configTableDBConfiguration']['configTableFieldsValues']['flaskHostAddress'] = config_table_host

            with open(json_address, 'w') as output_file:
                json.dump(data, output_file, indent=2)

        except FileNotFoundError as fileNotFoundErr:
            print("Error:", fileNotFoundErr)

    @staticmethod
    def get_creds_from_args():
        try:
            parser = argparse.ArgumentParser(description="Pass Database args in script")
            parser.add_argument('-a', '--address', required=False, help='DataBase Host Address', default="dbHost")
            parser.add_argument('-u', '--user_name', required=False, help='DataBase Username', default="username")
            parser.add_argument('-p', '--password', required=False, help='DataBase Password', default="password")
            parser.add_argument('-c', '--config_host', required=False, help='Config table host', default="host")
            db_args = parser.parse_args()
            db_host_address = db_args.address
            db_username = db_args.user_name
            db_user_password = db_args.password
            config_table_host = db_args.config_host
            # print(db_host_address, db_username, db_user_password, config_table_host)

            obj_update_config = UpdateDBCreds(str(db_host_address), str(db_username), str(db_user_password), str(config_table_host))
            obj_update_config.update_json_with_db()

        except UnboundLocalError as unLocalErr:
            print(unLocalErr)


obj_update_db_creds = UpdateDBCreds
obj_update_db_creds.get_creds_from_args()
