## Kubeflow Pipelines Scalability

The pipeline is scalable if we can calculate and predict the following:

* How much resources (how many K8s nodes and what type) we need to run N pipelines in parallel in T minutes
* How long it will take to run N pipelines in parallel with the given number of CPU and memory
* How many parallel pipelines we can run in T minutes with the given number of CPU and memory

So just by adding/reducing resources we can predictably change the numbers and durations. For example, we know that 500 parallel runs on 20 nodes take 3 hours. That means, assuming linear scalability, 1000 parallel runs will take approximately 6 hours. On the other hand, if we add 20 more nodes so there are 40 of them, then 1000 parallel runs will take 3 hours, same as 500 on 20 nodes.

In order to be able to answer the questions above we need to understand:

* How many resources (CPU and memory) is required for every single step in the pipeline
* How long it takes to run a single pipeline if it has all required resources
* How many pipelines we can run in parallel on a single node so the pipelines have all required resources

 
### Configure a training pool 

1. Configure a training node pool on a K8s cluster. 
    * That's important to run Kubeflow pipelines on a dedicated node pool so you can configure the size and autoscaling parameters of the pool according to your needs. 
    * Besides the regular node pool you may also consider:
       * [Spot Node Pool](https://docs.microsoft.com/en-us/azure/aks/spot-node-pool) to significantly reduce compute costs
       * [Virtual Node Pool](https://docs.microsoft.com/en-us/azure/aks/virtual-nodes-cli) to speed up provisioning resources for the new pods
    * Use your best guess to configure CPU and memory parameters of a node.
    * Specify a [taint for the node pool](https://docs.microsoft.com/azure/aks/use-multiple-node-pools#specify-a-taint-label-or-tag-for-a-node-pool) to prevent any pods to be scheduled on this pool except Kubeflow pipelines steps-pods. 
2. Make sure that KFP steps will run only on this training pool by adding a node selector constraint to every step. 
    * See [add_node_selector_constraint](https://kubeflow-pipelines.readthedocs.io/en/latest/_modules/kfp/dsl/_container_op.html?highlight=add_node_selector_constraint#)
    ```
    oper.add_node_selector_constraint('agentpool', 'trainingpool')        
    ```        
3. Make sure that KFP steps are allowed to run on this training pool by adding the toleration parameters to every step.
    * See [add_toleration](https://kubeflow-pipelines.readthedocs.io/en/latest/_modules/kfp/dsl/_container_op.html?highlight=add_toleration)
    ```
    oper.add_toleration(k8s_client.V1Toleration(key='sku', value='training', effect='NoSchedule'))
    ```

### Measure resources requests/limits
1. Make sure there is a node in the pool available. There is no workload on it.
2. Don't specify any resources requests/limits for the pipeline steps and run the pipeline
3. For every single step (see the pod name on KFP dashboard) monitor used CPU and memory. You can use:
    * Command line
    ```
        kubectl top pod pod_name -n kubeflow --containers
    ```
    * Training Performance Dashboard
4. Monitor the node utilization. You can use:
    * Command line.
    ```
        kubectl top nodes
    ```
    * Azure Monitor for Containers

    *Note*: If there is lack of memory the pod will be killed with OOM error and the pipeline will fail. If there is lack of CPU the pod will keep working, but slower than it should. So monitor node's CPU utilization. It should not get close to 90%. If it is the case, add more CPU to the node. 
5. Configure the resources requests and limits for every KFP step with set_cpu_request, set_cpu_limit, set_memory_request, set_memory_limit
```
            operations['datapreparation'] = dataprepare_op(
                data_scenario=scenario,
                kf_run_id = dsl.RUN_ID_PLACEHOLDER,
                output_storage_root = data_persistent_volume_path). \
                set_cpu_request('3'). \
                set_memory_request('24G'). \
                set_cpu_limit('4'). \
                set_memory_limit('24G')
```
* Setting the request makes sure that a pod won't be scheduled if either of the requested resources is not available. It will wait until it is available. It gives the predictable node utilization and makes sure the pod will have all resources it needs.
* Setting the limit makes the pod safe for the neighbors on the same node. So even if something happens inside the pod (e.g. memory leak, peak of CPU utilization) it will not eat all node's resources.
* Set the request to what you have monitored and round it up.
* Set the request equal to limit or upper if you expect potential raise of this parameter depending on input.

### Adjust node CPU and memory parameters

Consider adjusting CPU and memory parameters of a pool node. Perhaps your node is too big for a one job but too small to run multiple jobs in parallel.

### Implement the Orchestrator pipeline

Let's say your Kubeflow pipeline trains a model for a single use case or scenario. Each scenario is defined by a set of parameters that identify the datasource, training configurations, etc. 
So, in order to train a model for each of your multiple scenarios you need to run a pipeline multiple times with multiple sets of parameters values. 
In order to start and run all the required pipelines in parallel you might use an *orchestrator* pipeline. This pipeline may consist of a single step that reads parameters values for each scenario from a csv file and starts the training pipeline executions. Consider the following code snippet as a sample orchestration implementation:

```
def run_training_pipelines_for_scenarios(file_with_scenarios: str, kfp_client, pipeline_name, experiment_name):        
    # Read a csv file with scenarios and their paramaters
    csvfile = open(file_with_scenarios, 'r')

    # Create an experiment to contain all raining pipeline runs
    exp = kfp_client.create_experiment(experiment_name)    

    # Find a pipeline definition by name
    filter = json.dumps({'predicates': [{'key': 'name', 'op': 1, 'string_value': '{}'.format(pipeline_name)}]})
    pipelines = client.pipelines.list_pipelines(filter=filter)

    # Iterate over the scenarios list and start a training pipeline for each of them
    if (pipelines.pipelines):
        pipeline_id = pipelines.pipelines[0].id
        for row in csv.DictReader(csvfile):
            dict_row=dict(row)
            pipeline_params = {'scenario': json.dumps([dict_row])}
            kfp_run = client.run_pipeline(exp.id,
                        job_name=f'{row["id"]}-{row["scenario_name"]}',                                                
                        params=pipeline_params,
                        pipeline_id=pipeline_id)
```


### Calculate "jobs per node" ratio

1. Basing on a pool node parameters and configured resources requests estimate approximately how many jobs you can run in parallel on one node
2. Configure K8s autoscaling to have at least 2 nodes as a maximum number. 
3. Make sure that there is either 0 nodes in the pool or only 1 node and there is no workload on it. 
4. Run the estimated number of pipelines (with the orchestrator pipeline)
5. Monitor how many nodes in the pool are allocated 
    1. If there is still one node, increase the number of pipelines and run again. Keep exercising until you find the maximum number for one node.
    2. If there are two nodes, reduce the number of pipelines and run again. Keep exercising until you find the maximum number for one node. 

### Running multiple jobs in parallel

The *orchestrator* pipeline can also be a handy tool for performance testing with a generated csv file containing large amount of test scenarios.
* Create a script to generate a CSV file with any number of test scenarios
* Monitor the experiment and all pipeline runs in it with:
    * Command line
    ```
        kubectl top pod pod_name -n kubeflow --containers
        kubectl top nodes
    ```
    * Training Performance Dashboard


### Check the external bottlenecks

Let's say you have evaluated that you can run maximum 1 job on 1 node. Execution of 1 pipeline takes 10 minutes. It means that running 10 pipeline in parallel on 10 nodes should also take approximately 10 minutes. Unless there is an external concurrent resource (e.g. storage, database, etc.) used by all pipelines which can't serve the requests from all running pipelines in parallel. See the [performance testing report](performance-testing.md) showing how Kubeflow Pipelines can demonstrate linear scalability when there is no bottlenecks.   

### Known Bottleneck

KFP Minio storage. KFP uses Minio to store artifacts (pipelines, run_details, logs, etc.). The Minio instance, which is included in the default KFP installation, is backed up by pvc *minio-pvc* configured with 20Gi capacity.  When you run out of space the pipelines will start failing with a message "...unable to write outputs ... waiting for the condition ...". In order to extend *minio-pvc* do the following:

* Scaled down *minio* deployment
```
kubectl scale --replicas=0 deployment minio -n kubeflow
```

* Update *minio-pvc*
```
kubectl patch pvc minio-pvc -p '{ "spec": { "resources": { "requests": { "storage": "800Gi" }}}}' -n kubeflow
```
* Scaled up *minio* deployment
```
kubectl scale --replicas=1 deployment minio -n kubeflow
```


*Note*: It's been observed that after this resizing procedure (actually after restarting *minio* pod) KFP runs were failing on some nodes with a message "...unable to load outputs ... waiting for the condition ..." or "...unable to save outputs ... waiting for the condition ...". This is caused by connectivity issues when KFP steps could not connect to *minio* pod from some nodes. To avoid this, scale down the training node pool completely so the autoscaler will create new nodes under the load.

Consider also configuring the Minio storage as managed service. If you install Kubeflow pipelines with [Kustomize manifests for Azure](https://github.com/kubeflow/pipelines/pull/4567/files) it will do the job.  


### Evaluate K8s autoscaling set up

Being able to calculate how many nodes you need to run your maximum load in the required time, you can configure upper boundary of AKS autoscaling setup. For the periodic batch load the default AKS auto scaling configuration is good enough, however if the load is diverse, frequently changing from high peaks down to low activity, consider adjusting the [autoscaling profile](https://docs.microsoft.com/en-us/azure/aks/cluster-autoscaler#using-the-autoscaler-profile).



