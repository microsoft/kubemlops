import os
import kfp
from kfp import components
from kfp.dsl.extensions.kubernetes import use_secret
import kfp.compiler as compiler

component_root = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), ".")

queue_pipeline_op = components.load_component_from_file(os.path.join(component_root, 'azure\devops\queue_pipeline\component.yaml'))  # noqa: E501

def use_keyvault_secret_provider(volume_name='secrets-store-inline-2', secret_provider_class='azure-kvname', secret_volume_mount_path='/app/secrets'):
    def _use_keyvault_secret_provider(task):
        from kubernetes import client as k8s_client
        task = task.add_volume(
            k8s_client.V1Volume(
                name=volume_name,
                csi=k8s_client.V1CSIVolumeSource(
                    driver="secrets-store.csi.k8s.io",
                    read_only=True,
                    volume_attributes={
                        "secretProviderClass" : secret_provider_class
                        },
                    node_publish_secret_ref=k8s_client.V1LocalObjectReference(
                        name="secrets-store-creds"
                        )
                )
            )
        ).add_volume_mount(
                k8s_client.V1VolumeMount(
                    name=volume_name,
                    mount_path=secret_volume_mount_path,
                    read_only=True
                )
            )
        return task
    return _use_keyvault_secret_provider

def queue_az_pipeline():
    queue_task = queue_pipeline_op(
        organization='csedevops',
        project='Kubeflow Integration',
        id=304
    ).apply(use_keyvault_secret_provider())
    queue_task.execution_options.caching_strategy.max_cache_staleness = "P0D"

#compiler.Compiler().compile(queue_az_pipeline, 'pipeline.zip')

kfp.Client(host="http://127.0.0.1:8080/").create_run_from_pipeline_package("C:\kubemlops\code\pipeline.zip", arguments={})

#kfp.Client(host="http://127.0.0.1:8080/").create_run_from_pipeline_func(queue_az_pipeline, arguments={})