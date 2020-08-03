def use_databricks_secret(secret_name='databricks-secret'):
    def _use_databricks_secret(task):
        from kubernetes import client as k8s_client
        (
            task.container
                .add_env_variable(
                    k8s_client.V1EnvVar(
                        name='DATABRICKS_HOST',
                        value_from=k8s_client.V1EnvVarSource(
                            secret_key_ref=k8s_client.V1SecretKeySelector(
                                name=secret_name,
                                key='DATABRICKS_HOST'
                            )
                        )
                    )
                )
                .add_env_variable(  # noqa: E131
                    k8s_client.V1EnvVar(
                        name='DATABRICKS_TOKEN',
                        value_from=k8s_client.V1EnvVarSource(
                            secret_key_ref=k8s_client.V1SecretKeySelector(
                                name=secret_name,
                                key='DATABRICKS_TOKEN'
                            )
                        )
                    )
                )
                .add_env_variable(  # noqa: E131
                    k8s_client.V1EnvVar(
                        name='CLUSTER_ID',
                        value_from=k8s_client.V1EnvVarSource(
                            secret_key_ref=k8s_client.V1SecretKeySelector(
                                name=secret_name,
                                key='CLUSTER_ID'
                            )
                        )
                    )
                )
        )
        return task
    return _use_databricks_secret


def use_kfp_host_secret(secret_name='kfp-host-secret'):
    def _use_kfp_host_secret(task):
        from kubernetes import client as k8s_client
        (
            task.container
                .add_env_variable(
                    k8s_client.V1EnvVar(
                        name='KFP_HOST',
                        value_from=k8s_client.V1EnvVarSource(
                            secret_key_ref=k8s_client.V1SecretKeySelector(
                                name=secret_name,
                                key='KFP_HOST'
                            )
                        )
                    )
                )
        )
        return task
    return _use_kfp_host_secret


def use_image(image_name):
    def _use_image(task):
        task.image = image_name
        return task
    return _use_image

def use_keyvault_secret_provider(volume_name='secrets-store-inline', secret_provider_class='azure-kvname', secret_volume_mount_path='/app/secrets'):
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
                        }
                    node_publish_secret_ref=k8s_client.V1LocalObjectReference(
                        name="secrets-store-creds"
                        )
                )
            )
        ).add_volume_mount(
                k8s_client.V1VolumeMount(
                    name=volume_name,
                    mount_path=secret_volume_mount_path
                )
            )
        return task
    return _use_keyvault_secret_provider
