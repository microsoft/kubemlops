#!/bin/bash
#set -x

# https://argoproj.github.io/argo-cd/getting_started/

while getopts :n:r:s: option; do
    case "${option}" in
    n) ARGO_CD_NAMESPACE=${OPTARG} ;;
    r) REPO_URL=${OPTARG} ;;
    s) SSH_PRIVATE_KEY_PATH=${OPTARG} ;;
    *)
        echo "Please refer to usage guide on GitHub" >&2
        exit 1
        ;;
    esac
done

echo "ARGO_CD_NAMESPACE: $ARGO_CD_NAMESPACE"
echo "REPO_URL: $REPO_URL"
echo "SSH_PRIVATE_KEY_PATH: $SSH_PRIVATE_KEY_PATH"

# Deploy ArgoCD to connected k8s cluster
kubectl create namespace $ARGO_CD_NAMESPACE
kubectl config set-context --current --namespace $ARGO_CD_NAMESPACE
kubectl apply -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

# Get pod name
ARGO_SERVER_POD_NAME=$(kubectl get pods -l app.kubernetes.io/name=argocd-server -o name | cut -d'/' -f 2)

# OPTIONAL - Patch svc to LoadBalancer so it is more easily accessed
# kubectl apply -f argocd-server-loadbalancer.yaml

# Portforward to access UI/connect CLI
while [[ $(kubectl get pods -l app.kubernetes.io/name=argocd-server -o 'jsonpath={..status.conditions[?(@.type=="Ready")].status}') != "True" ]]; do echo "waiting for argocd-server pod." && sleep 3; done
kubectl port-forward svc/argocd-server 8080:443 &
PORT_FORWARD_PID=$!
sleep 3
# Login - default username is 'admin', password is podname. Can be changed via: argocd account update-password
echo "Logging into ArgoCD CLI"
argocd login localhost:8080 --username admin --password $ARGO_SERVER_POD_NAME --insecure

# add source repo for gitops
echo "Adding $REPO_URL to ArgoCD"
argocd repo add $REPO_URL \
    --ssh-private-key-path $SSH_PRIVATE_KEY_PATH

# Won't do this here, but this is how to add an example application through the cli
# argocd app create guestbook --repo https://github.com/argoproj/argocd-example-apps.git --path guestbook --dest-server https://kubernetes.default.svc --dest-namespace default

# Optional - register external clusters -
# https://argoproj.github.io/argo-cd/getting_started/#5-register-a-cluster-to-deploy-apps-to-optional

# Cleanup
kill $PORT_FORWARD_PID
echo "Successfully installed ArgoCD on the connected cluster!"
