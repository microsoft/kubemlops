#!/bin/bash
#set -x

# https://argoproj.github.io/argo-cd/getting_started/

# Deploy ArgoCD to connected k8s cluster
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

# Set context
kubectl config set-context --current --namespace argocd

# Get pod name
ARGO_SERVER_POD_NAME=$(kubectl get pods -n argocd -l app.kubernetes.io/name=argocd-server -o name | cut -d'/' -f 2)

# OPTIONAL - Patch svc to LoadBalancer so it is more easily accessed
# kubectl apply -f argocd-server-loadbalancer.yaml

# Portforward to access UI/connect CLI
sleep 5
kubectl port-forward svc/argocd-server -n argocd 8080:443 &
PORT_FORWARD_PID=$!
sleep 3
# Login - default username is 'admin', password is podname. Can be changed via: argocd account update-password
argocd login localhost:8080 --username admin --password $ARGO_SERVER_POD_NAME --insecure

# TODO: add repo credentials 
# argocd repo or repocreds
# argocd repo add git@github.com:argoproj/argocd-example-apps.git --ssh-private-key-path ~/.ssh/id_rsa

# TODO: Add application individually?
# argocd app create guestbook --repo https://github.com/argoproj/argocd-example-apps.git --path guestbook --dest-server https://kubernetes.default.svc --dest-namespace default

## Optional - register external clusters -
# https://argoproj.github.io/argo-cd/getting_started/#5-register-a-cluster-to-deploy-apps-to-optional

# Cleanup
kill $PORT_FORWARD_PID
scho "Successfully installed ArgoCD on the connected cluster!"


