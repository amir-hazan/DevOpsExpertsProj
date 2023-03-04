import platform
import sys
import os
import argparse
import ruamel.yaml

# define root source path
package_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.append(package_path)


class SetReplicasCountInValuesYaml:
    """ update values yaml - replicaCount """
    @staticmethod
    def get_build_num_from_script_args():
        try:
            parser = argparse.ArgumentParser(description="Replicas count for Helm chart")
            parser.add_argument("-r",
                                "--replicaCount",
                                required=False,
                                type=int,
                                help='Build Number from Jenkins Pipeline',
                                default="1"
                                )

            replica_count_args = parser.parse_args()
            replica_count_args = replica_count_args.replicaCount

        except UnboundLocalError as unLocalErr:
            print(unLocalErr)

        finally:
            return replica_count_args

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
    def update_replicas_values_yaml():

        try:
            yaml = ruamel.yaml.YAML()
            values_yaml_file = SetReplicasCountInValuesYaml.get_yaml_file()

            with open(values_yaml_file, 'r') as f:  # get current replicas count
                yaml_output = yaml.load(f)

            yaml_replica_count = yaml_output['replicaCount']
            print("current replicaCount:", yaml_replica_count)

            replica_count_from_args = SetReplicasCountInValuesYaml.get_build_num_from_script_args()
            yaml_output['replicaCount'] = int(replica_count_from_args)
            print("new replicaCount:", replica_count_from_args)

            with open(values_yaml_file, 'w') as f:  # update new replica counts number
                yaml.dump(yaml_output, f)

        except Exception as e:
            print(f"Error occurred:", e)

        finally:
            exit(0)


SetReplicasCountInValuesYaml.update_replicas_values_yaml()
