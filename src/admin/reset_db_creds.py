import sys
import os

# define root source path
package_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.append(package_path)

import json
import platform


class ResetDBCreds:
    """ reset json db creds to empty strings """

    @staticmethod
    def reset_db_creds_from_json():

        try:
            if platform.system() == 'Windows':
                config_path = package_path + '\\src\\Config\\Config.json'
            elif platform.system() == 'Darwin' or platform.system() == 'Linux':
                config_path = package_path + '/src/Config/Config.json'

            json_address = str(config_path)
            with open(json_address, 'r') as json_file:
                data = json.load(json_file)

                data['DevOpsExpertsProj']['generalDBConfiguration']['dbHost'] = None
                data['DevOpsExpertsProj']['generalDBConfiguration']['dbUserName'] = None
                data['DevOpsExpertsProj']['generalDBConfiguration']['dbUserPassword'] = None
                data['DevOpsExpertsProj']['configTableDBConfiguration']['configTableFieldsValues']['flaskHostAddress'] = None

            with open(json_address, 'w') as output_file:
                json.dump(data, output_file, indent=2)

                print("dbHost:", data['DevOpsExpertsProj']['generalDBConfiguration']['dbHost'])
                print("dbUserName:", data['DevOpsExpertsProj']['generalDBConfiguration']['dbUserName'])
                print("dbUserPassword:", data['DevOpsExpertsProj']['generalDBConfiguration']['dbUserPassword'])
                print("configTableHost:", data['DevOpsExpertsProj']['configTableDBConfiguration']['configTableFieldsValues']['flaskHostAddress'])

        except FileNotFoundError as fileNotFoundErr:
            print("Error:", fileNotFoundErr)


obj_reset_db_creds = ResetDBCreds
obj_reset_db_creds.reset_db_creds_from_json()
