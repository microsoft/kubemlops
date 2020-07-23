# flake8: noqa E501
# "KubeFlow Pipeline with AzureDevops Callback"
import os
from kubernetes import client as k8s_client
import kfp.dsl as dsl
import kfp.compiler as compiler
import kfp.components as components
from kfp.azure import use_azure_secret
from kubernetes.client.models import V1EnvVar
from utils.kfp_helper import use_databricks_secret, use_image, use_kfp_host_secret


persistent_volume_path = '/mnt/azure'
batch = 32
model_name = 'tacosandburritos'
operations = {}
image_size = 160
training_folder = 'train'
training_dataset = 'train.txt'
model_folder = 'model'
image_repo_name = "kubeflowyoacr.azurecr.io/mexicanfood"
mlflow_url = 'http://mlflow:5000'

component_root = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), ".")
image_repo_name = "kubeflowyoacr.azurecr.io/mexicanfood"

mlflow_project_op = components.load_component_from_file(os.path.join(component_root, 'mlflow-project/component.yaml'))  # noqa: E501
mlflow_project_image_name = image_repo_name + '/mlflowproject:%s' % (os.getenv('MLFLOWPROJECT_TAG') or 'latest')  # noqa: E501

train_op = components.load_component_from_file(os.path.join(component_root, 'training/component.yaml'))  # noqa: E501
train_image_name = image_repo_name + '/training:%s' % (os.getenv('TRAINING_TAG') or 'latest')  # noqa: E501

evaluate_op = components.load_component_from_file(os.path.join(component_root, 'evaluate/component.yaml'))  # noqa: E501

register_op = components.load_component_from_file(os.path.join(component_root, 'register/component.yaml'))  # noqa: E501
register_images_name = image_repo_name + '/register:%s' % (os.getenv('REGISTER_TAG') or 'latest')  # noqa: E501

register_mlflow_op = components.load_component_from_file(os.path.join(component_root, 'register-mlflow/component.yaml'))  # noqa: E501
register_mlflow_image_name = image_repo_name + '/register-mlflow:%s' % (os.getenv('REGISTERMLFLOW_TAG') or 'latest')  # noqa: E501

exit_op = components.load_component_from_file(os.path.join(component_root, 'azdocallback/component.yaml'))  # noqa: E501
exit_image_name = image_repo_name + '/azdocallback:%s' % (os.getenv('AZDOCALLBACK_TAG') or 'latest')  # noqa: E501

preprocess_op = components.load_component_from_file(os.path.join(component_root, 'preprocess/component.yaml'))  # noqa: E501
preprocess_image_name = image_repo_name + '/preprocess:%s' % (os.getenv('PREPROCESS_TAG') or 'latest')  # noqa: E501


@dsl.pipeline(
    name='Tacos vs. Burritos',
    description='Simple TF CNN'
)
def tacosandburritos_train(
    resource_group,
    workspace,
    dataset,
    mlflow_experiment_id,
    azdocallbackinfo=None
):

    exit_handler_op = exit_op(kfp_host_url="$(KFP_HOST)",
                              azdocallbackinfo=azdocallbackinfo,
                              run_id=dsl.RUN_ID_PLACEHOLDER,
                              tenant_id="$(AZ_TENANT_ID)",
                              service_principal_id="$(AZ_CLIENT_ID)",
                              service_principal_password="$(AZ_CLIENT_SECRET)").apply(use_azure_secret()).apply(use_kfp_host_secret()).apply(use_image(exit_image_name))  # noqa: E501

    with dsl.ExitHandler(exit_op=exit_handler_op):

        operations['mlflowproject'] = mlflow_project_op(mlflow_experiment_id=mlflow_experiment_id,  # noqa: E501
                                                        kf_run_id=dsl.RUN_ID_PLACEHOLDER).apply(use_databricks_secret()).apply(use_image(mlflow_project_image_name))  # noqa: E501

        operations['preprocess'] = preprocess_op(base_path=persistent_volume_path,  # noqa: E501
                                                 training_folder=training_folder,  # noqa: E501
                                                 target=training_dataset,
                                                 image_size=image_size,
                                                 zipfile=dataset).apply(use_image(preprocess_image_name))  # noqa: E501

        operations['preprocess'].after(operations['mlflowproject'])  # noqa: E501

        operations['training'] = train_op(base_path=persistent_volume_path,
                                          training_folder=training_folder,
                                          epochs=2,
                                          batch=batch,
                                          image_size=image_size,
                                          lr=0.0001,
                                          model_folder=model_folder,
                                          images=training_dataset,
                                          dataset=operations['preprocess'].outputs['dataset']). \
            set_memory_request('16G'). \
            add_env_variable(V1EnvVar(name="RUN_ID", value=dsl.RUN_ID_PLACEHOLDER)). \
            add_env_variable(V1EnvVar(name="MLFLOW_TRACKING_URI", value=mlflow_url)). \
            add_env_variable(V1EnvVar(name="GIT_PYTHON_REFRESH", value='quiet')). \
            apply(use_image(train_image_name))

        operations['training'].after(operations['preprocess'])

        operations['evaluate'] = evaluate_op(
            model=operations['training'].outputs['model'])
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
            apply(use_image(register_images_name))

        operations['register to AML'].after(operations['evaluate'])

        operations['register to mlflow'] = register_mlflow_op(model='model',
                                                              model_name=model_name,
                                                              experiment_name='mexicanfood',
                                                              run_id=dsl.RUN_ID_PLACEHOLDER). \
            apply(use_azure_secret()). \
            add_env_variable(V1EnvVar(name="MLFLOW_TRACKING_URI", value=mlflow_url)). \
            apply(use_image(register_mlflow_image_name))

        operations['register to mlflow'].after(operations['register to AML'])

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


if __name__ == '__main__':
    compiler.Compiler().compile(tacosandburritos_train, 'pipeline.tar.gz')
