# flake8: noqa E501
# "KubeFlow Pipeline with AzureDevops Callback"
import os
from kubernetes import client as k8s_client
import kfp
import kfp.dsl as dsl
import kfp.compiler as compiler
import kfp.components as components
from kfp.azure import use_azure_secret
from kubernetes.client.models import V1EnvVar
from utils.kfp_helper import use_databricks_secret, use_image, use_kfp_host_secret
from utils.azure_auth import get_access_token
from dotenv import load_dotenv
import uuid
import subprocess

persistent_volume_path = '/mnt/azure'
operations = {}

component_root = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), ".")
image_repo_name = "kubeflowyoacr.azurecr.io/mexicanfood"

notebook_op = components.load_component_from_file(os.path.join(component_root, 'components/notebook-comp/component.yaml'))  # noqa: E501
notebook_images_name = image_repo_name + '/notebook-comp:latest'  # noqa: E501


@dsl.pipeline(
    name='Tacos vs. Burritos',
    description='Simple TF CNN'
)
def tacosandburritos_train():

    operations['local-comp'] = notebook_op(train_data_path='train_data_for_exp'). \
        apply(use_azure_secret()). \
        apply(use_image(notebook_images_name))

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
    token = get_access_token(os.environ.get("TENANT_ID"), os.environ.get("SP_APP_ID"), os.environ.get("SP_APP_SECRET"))  # noqa: E501
    client = kfp.Client(os.environ.get("KFP_HOST"), existing_token=token)
    pipeline_file = os.path.join('pipeline.tar.gz')
    pipeline_name = os.environ.get("PIPELINE_NAME") + "-" + str(uuid.uuid4())
    pipeline = client.pipeline_uploads.upload_pipeline(pipeline_file, name=pipeline_name)  # noqa: E501
    exp = client.get_experiment(experiment_name=os.environ.get("EXP_NAME"))  # noqa: E501
    # pipeline_params = {}
    # pipeline_params["paramname"] = paramvalue
    client.run_pipeline(exp.id, job_name=os.environ.get("RUN_NAME"),
                        pipeline_id=pipeline.id)
