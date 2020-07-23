# Initialize variables:
# KFP_HOST=
# KUBEFLOW_NAMESPACE=kubeflow

kubectl create secret generic kfp-host-secret --from-literal=KFP_HOST=$KFP_HOST -n $KUBEFLOW_NAMESPACE
