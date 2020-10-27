# flake8: noqa E501
"""Main pipeline file"""
from kubernetes import client as k8s_client
import kfp.dsl as dsl
import kfp.compiler as compiler
import kfp.components as components
from kfp.azure import use_azure_secret
import json
import os
from kubernetes.client.models import V1EnvVar
from utils.kfp_helper import use_databricks_secret, use_image

TRAIN_START_EVENT = "Training Started"
TRAIN_FINISH_EVENT = "Training Finished"


def get_callback_payload(event_type):
    payload = {}
    payload['event_type'] = event_type
    payload['sha'] = os.getenv('GITHUB_SHA')
    payload['pr_num'] = os.getenv('PR_NUM')
    payload['run_id'] = dsl.RUN_ID_PLACEHOLDER
    if (event_type == TRAIN_FINISH_EVENT):
        payload['status'] = '{{workflow.status}}'
    return json.dumps(payload)


def get_start_callback_container():
    return dsl.UserContainer('callback',
                             'curlimages/curl',
                             command=['curl'],
                             args=['-d',
                                get_callback_payload(TRAIN_START_EVENT), callback_url])  # noqa: E501


persistent_volume_path = '/mnt/azure'
batch = 32
model_name = 'tacosandburritos'
operations = {}
image_size = 160
training_folder = 'train'
training_dataset = 'train.txt'
model_folder = 'model'
callback_url = 'kubemlopsbot-svc.kubeflow.svc.cluster.local:8080'
mlflow_url = 'http://mlflow:5000'

component_root = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), ".")
image_repo_name = "kubeflowyoacr.azurecr.io/mexicanfood"

databricks_op = components.load_component_from_file(os.path.join(component_root, 'databricks/component.yaml'))  # noqa: E501
databricks_image_name = image_repo_name + '/databricks-notebook:%s' % (os.getenv('DATABRICKS_TAG') or 'latest')  # noqa: E501

preprocess_op = components.load_component_from_file(os.path.join(component_root, 'preprocess/component.yaml'))  # noqa: E501
preprocess_image_name = image_repo_name + '/preprocess:%s' % (os.getenv('PREPROCESS_TAG') or 'latest')  # noqa: E501

train_op = components.load_component_from_file(os.path.join(component_root, 'training/component.yaml'))  # noqa: E501
train_image_name = image_repo_name + '/training:%s' % (os.getenv('TRAINING_TAG') or 'latest')  # noqa: E501

evaluate_op = components.load_component_from_file(os.path.join(component_root, 'evaluate/component.yaml'))  # noqa: E501
register_op = components.load_component_from_file(os.path.join(component_root, 'aml-register-model/component.yaml'))  # noqa: E501
register_images_name = image_repo_name + '/aml-register-model:%s' % (os.getenv('AML_REGISTER_MODEL_TAG') or 'latest')  # noqa: E501

register_mlflow_op = components.load_component_from_file(os.path.join(component_root, 'register-mlflow/component.yaml'))  # noqa: E501
register_mlflow_image_name = image_repo_name + '/register-mlflow:%s' % (os.getenv('REGISTERMLFLOW_TAG') or 'latest')  # noqa: E501

finalize_op = components.load_component_from_file(os.path.join(component_root, 'finalize/component.yaml'))  # noqa: E501
exit_op = components.load_component_from_file(os.path.join(component_root, 'exit-handler/component.yaml'))  # noqa: E501


@dsl.pipeline(
    name='Tacos vs. Burritos',
    description='Simple TF CNN'
)
def tacosandburritos_train(
    resource_group,
    workspace,
    dataset
):

    exit_handler = exit_op(callback_url=callback_url,
                           callback_payload=get_callback_payload(TRAIN_FINISH_EVENT))

    with dsl.ExitHandler(exit_handler):

        operations['data processing on databricks'] = databricks_op(run_id=dsl.RUN_ID_PLACEHOLDER,  # noqa: E501
                                                 notebook_params='{"argument_one":"param one","argument_two":"param two"}'  # noqa: E501
                                                 ).apply(use_databricks_secret()). \
                                                 add_init_container(get_start_callback_container()). \
                                                 set_memory_request('100M'). \
                                                 set_memory_limit('200M'). \
                                                 apply(
                                                     use_image(databricks_image_name))

        operations['preprocess'] = preprocess_op(base_path=persistent_volume_path,  # noqa: E501
                                                 training_folder=training_folder,  # noqa: E501
                                                 target=training_dataset,
                                                 image_size=image_size,
                                                 zipfile=dataset). \
                                                 set_memory_request('500M'). \
                                                 set_memory_limit('750M'). \
                                                 apply(
                                                     use_image(preprocess_image_name))

        operations['preprocess'].after(operations['data processing on databricks'])  # noqa: E501

        operations['training'] = train_op(base_path=persistent_volume_path,
                                            training_folder=training_folder,
                                            epochs=2,
                                            batch=batch,
                                            image_size=image_size,
                                            lr=0.0001,
                                            model_folder=model_folder,
                                            images=training_dataset,
                                            dataset=operations['preprocess'].outputs['dataset']). \
                                          set_memory_request('5G'). \
                                          set_memory_limit('6G'). \
                                          add_env_variable(V1EnvVar(name="RUN_ID", value=dsl.RUN_ID_PLACEHOLDER)). \
                                          add_env_variable(V1EnvVar(name="MLFLOW_TRACKING_URI", value=mlflow_url)). \
                                          add_env_variable(V1EnvVar(name="GIT_PYTHON_REFRESH", value='quiet')). \
                                          apply(use_image(train_image_name))  # noqa: E501, E127

        operations['training'].after(operations['preprocess'])

        operations['evaluate'] = evaluate_op(
            model=operations['training'].outputs['model']). \
            set_memory_request('25M'). \
            set_memory_limit('50M')
        operations['evaluate'].after(operations['training'])

        operations['register to AML'] = register_op(base_path=persistent_volume_path,
                                          model_file='latest.h5',
                                          model_name=model_name,
                                          tenant_id='$(AZ_TENANT_ID)',
                                          service_principal_id='$(AZ_CLIENT_ID)',
                                          service_principal_password='$(AZ_CLIENT_SECRET)',
                                          subscription_id='$(AZ_SUBSCRIPTION_ID)',
                                          resource_group=resource_group,
                                          workspace=workspace,
                                          run_id=dsl.RUN_ID_PLACEHOLDER). \
                                        apply(use_azure_secret()). \
                                        set_memory_request('100M'). \
                                        set_memory_limit('200M'). \
                                        apply(use_image(register_images_name))  # noqa: E501, E127

        operations['register to AML'].after(operations['evaluate'])

        operations['register to mlflow'] = register_mlflow_op(model='model',
                                                              model_name=model_name,
                                                              experiment_name='mexicanfood',
                                                              run_id=dsl.RUN_ID_PLACEHOLDER). \
                                                            apply(use_azure_secret()). \
                                                            add_env_variable(V1EnvVar(name="MLFLOW_TRACKING_URI", value=mlflow_url)). \
                                                            set_memory_request('100M'). \
                                                            set_memory_limit('200M'). \
                                                            apply(use_image(register_mlflow_image_name))  # noqa: E501

        operations['register to mlflow'].after(operations['register to AML'])

        operations['finalize'] = finalize_op(callback_url=callback_url,
                                              callback_payload=get_callback_payload("Model is registered")). \
                                            set_memory_request('100M'). \
                                            set_memory_limit('200M')
        operations['finalize'].after(operations['register to mlflow'])

    for _, op_1 in operations.items():
        op_1.container.set_image_pull_policy("Always")
        op_1.add_volume(
            k8s_client.V1Volume(
              name='azure',
              persistent_volume_claim=k8s_client.V1PersistentVolumeClaimVolumeSource(  # noqa: E501
                claim_name='azure-managed-file')
            )
        ).add_volume_mount(k8s_client.V1VolumeMount(
            mount_path='/mnt/azure', name='azure'))
        # Specify training node pool affinity
        op_1.add_node_selector_constraint('agentpool', 'training')
        # Allow all steps to be scheduled on the training node pool
        op_1.add_toleration(k8s_client.V1Toleration(key='sku', value='training', effect='NoSchedule'))


if __name__ == '__main__':
    compiler.Compiler().compile(tacosandburritos_train, __file__ + '.tar.gz')
