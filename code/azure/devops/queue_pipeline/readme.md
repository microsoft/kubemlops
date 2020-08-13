# Queue Pipeline Task

This task enables you to queue an [Azure Pipelines](https://docs.microsoft.com/en-us/azure/devops/pipelines/?view=azure-devops) pipeline from a Kubeflow pipeline. For example, this task may be used to queue the deployment of a model via Azure Pipelines after the model is trained and registered by the Kubeflow pipeline.

## Inputs

|Name|Type|Required|Description|
|---|---|---|---|
|organization|string|Y|The Azure DevOps organization that contains the pipeline to be queued. https[]()://dev.azure.com/`organization`/project/_build?definitionId=id|
|project|string|Y|The Azure DevOps project that contains the pipeline to be queued. https[]()://dev.azure.com/organization/`project`/_build?definitionId=id|
|id|string|Y|The id of the pipeline definition to queue. Shown in the url as *pipelineId* or *definitionId*. https[]()://dev.azure.com/organization/project/_build?definitionId=`id`|
|pat_env|string|one of pat_env or pat_path_env|The name of the environment variable containing the PAT for Azure Pipelines authentication|
|pat_path_env|string|one of pat_env or pat_path_env|The name of the environment variable containing a path to the PAT for Azure Pipelines authentication|
|sourch_branch|string||The branch of the source code for queuing the pipeline.|
|source_version|string||The version (e.g. commit id) of the source code for queuing the pipeline.|
|parameters|string||Json serialized string of key-values pairs e.g. `{ 'x': '1', 'y': '2' }`. These values can be accessed as `$(x)` and `$(y)` in the Azure Pipelines pipeline.|

## Outputs

The uri for the newly queued build is written to the log.

## Usage

```python
import os
import kfp
from kfp import components
from kfp.dsl.extensions.kubernetes import use_secret
import kfp.compiler as compiler
from kubernetes import client as k8s_client

component_root = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), ".")

queue_pipeline_op = components.load_component_from_file(os.path.join(component_root, 'azure\devops\queue_pipeline\component.yaml'))

def queue_az_pipeline():
    secret_name = "azdopat"
    secret_path = "/app/secrets"
    pat_path_env = "PAT_PATH"
    secret_file_path_in_volume = "azdopat"
    organization = # organization
    project = # project
    pipeline_id = # id
    queue_task = queue_pipeline_op(
        organization=organization,
        project=project,
        id=pipeline_id,
        pat_path_env=pat_path_env
    ).apply(use_secret(secret_name=secret_name, secret_volume_mount_path=secret_path))

    # path separator workaround when compiling on windows
    queue_task.container.add_env_variable(
        k8s_client.V1EnvVar(
            name=pat_path_env,
            value=secret_path + "/" + secret_file_path_in_volume
        ))

kfp.Client().create_run_from_pipeline_func(queue_az_pipeline, arguments={})
```
