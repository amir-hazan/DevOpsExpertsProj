import platform
import sys
import os
import argparse
import ruamel.yaml

# define root source path
package_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.append(package_path)


class SetTagVersionInHelmValues:
    """ update values yaml - so it will always use the latest build number from dockerHub """
    @staticmethod
    def get_build_num_from_script_args():
        try:
            parser = argparse.ArgumentParser(description="Docker image tag number from Jenkins Pipeline")
            parser.add_argument("-b",
                                "--buildNumber",
                                required=False,
                                type=int,
                                help='Build Number from Jenkins Pipeline',
                                default="1"
                                )

            build_num_args = parser.parse_args()
            build_num_args = build_num_args.buildNumber

        except UnboundLocalError as unLocalErr:
            print(unLocalErr)

        finally:
            return build_num_args

    @staticmethod
    def get_yaml_file():
        """ open values.yaml file """
        try:
            if platform.system() == 'Windows':
                yaml_values_file = package_path + '\\devops-experts-proj-chart\\values.yaml'
            elif platform.system() == 'Darwin' or platform.system() == 'Linux':
                yaml_values_file = package_path + '/devops-experts-proj-chart/values.yaml'

        except FileNotFoundError as fNotFound:
            print("FileNotFoundErr:", fNotFound)

        return yaml_values_file

    @staticmethod
    def update_values_yaml():

        try:
            yaml = ruamel.yaml.YAML()
            values_yaml_file = SetTagVersionInHelmValues.get_yaml_file()

            with open(values_yaml_file, 'r') as f:  # get current tag version from values.yaml
                yaml_output = yaml.load(f)

            yaml_tag_version = yaml_output['pythonFlaskApp']["tagVersion"]
            print("current image tag version:", yaml_tag_version)

            build_number_from_args = SetTagVersionInHelmValues.get_build_num_from_script_args()
            yaml_output['pythonFlaskApp']["tagVersion"] = int(build_number_from_args)
            print("new image tag version:", build_number_from_args)

            with open(values_yaml_file, 'w') as f:  # update new tag ver based on build number from Jenkins pipeline
                yaml.dump(yaml_output, f)

        except Exception as e:
            print(f"Error occurred:", e)

        finally:
            exit(0)


SetTagVersionInHelmValues.update_values_yaml()
