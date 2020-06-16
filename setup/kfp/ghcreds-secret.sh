kubectl create secret generic ghcreds-secret --from-literal=GITHUB_TOKEN=$GITHUB_TOKEN --from-literal=GITHUB_REPOSITORY=$GITHUB_REPOSITORY -n $KUBEFLOW_NAMESPACE
