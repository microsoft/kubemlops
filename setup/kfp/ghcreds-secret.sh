export GITHUB_TOKEN=''
export GITHUB_REPOSITORY='kaizentm/kubemlops'
export NAMESPACE='kubeflow'
kubectl create secret generic ghcreds-secret --from-literal=GITHUB_TOKEN=$GITHUB_TOKEN --from-literal=GITHUB_REPOSITORY=$GITHUB_REPOSITORY -n $NAMESPACE
