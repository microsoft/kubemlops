export DATABRICKS_HOST=''
export DATABRICKS_TOKEN=''
export CLUSTER_ID=''
export NAMESPACE='kubeflow'
kubectl create secret generic databricks-secret --from-literal=DATABRICKS_HOST=$DATABRICKS_HOST --from-literal=DATABRICKS_TOKEN=$DATABRICKS_TOKEN --from-literal=CLUSTER_ID=$CLUSTER_ID -n $NAMESPACE
