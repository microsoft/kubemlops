# Initialize variables:
# GITHUB_TOKEN=
# GITHUB_REPOSITORY=
# KUBEFLOW_NAMESPACE=kubeflow

kubectl create secret generic ghcreds-secret --from-literal=GITHUB_TOKEN=$GITHUB_TOKEN --from-literal=GITHUB_REPOSITORY=$GITHUB_REPOSITORY -n $KUBEFLOW_NAMESPACE
