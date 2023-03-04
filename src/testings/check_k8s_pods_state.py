import os
import platform
import sys
from kubernetes import client, config
from dotenv import load_dotenv
import time

# define root source path
package_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.append(package_path)


class CheckDeploymentPodsState:

    @staticmethod
    def get_helm_namespace():

        """ get namespace from .env file """
        try:
            if platform.system() == 'Windows':
                env_file_path = package_path + "\\.env"
            elif platform.system() == 'Darwin' or platform.system() == 'Linux':
                env_file_path = package_path + "/.env"

            load_dotenv(env_file_path)

        except AttributeError as e:
            print("An AttributeError occurred:", e)
            return False

        except Exception as err:
            print("Exception:", err)
            return False

        finally:
            namespace = os.getenv("HELM_CHART_NAMESPACE")

        return namespace

    @staticmethod
    def check_pods_status():
        config.load_kube_config()
        v1 = client.CoreV1Api()

        namespace = CheckDeploymentPodsState.get_helm_namespace()

        try:
            v1.read_namespace(namespace)
        except client.exceptions.ApiException as e:
            if e.status == 404:
                print(f"Namespace {namespace} not found. Exiting script.")
                sys.exit(1)

        while True:

            pods = v1.list_namespaced_pod(namespace)
            num_pods = len(pods.items)

            num_running_pods = 0

            for pod in pods.items:
                if pod.status.phase == "Running":
                    print("pod number:", num_running_pods, "pod name:", pod.metadata.name, "pod state:", pod.status.phase)
                    num_running_pods += 1
                    time.sleep(5)
                # elif pod.status.phase == "Terminating":
                #     print("pod:", pod.metadata.name, "state:", pod.status.phase)
                #     time.sleep(10)

            if num_pods != 0 and num_pods == num_running_pods:
                print("\nAll pods are in the 'Running' state")
                sys.exit(0)

            # If not all pods are in the "Running" state, wait for 10 seconds before checking again
            print("Waiting for all pods to be in the 'Running' state...")
            time.sleep(10)


CheckDeploymentPodsState.check_pods_status()
