#!/bin/bash
#set -x

# https://argoproj.github.io/docs/argo/getting-started.html

# Installing Argo CLI for linux
# wget https://github.com/argoproj/argo/releases/download/v2.7.5/argo-linux-amd64 -O ~/tmp/argo
# chmod +x ~/tmp/argo
# sudo mv ~/tmp/argo /usr/local/bin

# Deploy Argo to connected k8s cluster
kubectl create namespace argodev

# Set context
# kubectl config set-context --current --namespace argodev

kubectl apply -f https://raw.githubusercontent.com/argoproj/argo/stable/manifests/install.yaml --namespace argodev
kubectl create rolebinding default-admin --clusterrole=admin --serviceaccount=argodev:default --namespace argodev

# role for argo-server
kubectl create rolebinding argodev-admin --clusterrole=admin --serviceaccount=argodev:argo-server --namespace argodev
# role for workflow-controller
kubectl create rolebinding argo-read --clusterrole=admin --serviceaccount=argodev:argo --namespace argodev

# default role for admin permissions.
# kubectl create rolebinding default-admin --clusterrole=admin --serviceaccount=default:default --namespace argodev

# Helm Install minio to hold argo artifacts
# helm repo add stable https://kubernetes-charts.storage.googleapis.com
# helm repo update
helm install argo-artifacts stable/minio \
  --namespace argodev \
  --set service.type=ClusterIP \
  --set defaultBucket.enabled=true \
  --set defaultBucket.name=my-bucket \
  --set persistence.enabled=false \
  --set fullnameOverride=argo-artifacts
# https://github.com/helm/charts/tree/master/stable/minio
# TODO: Set accessKey (default): AKIAIOSFODNN7EXAMPLE
# TODO: Set secretKey (default): wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY 

# config map for minio s3 bucket
kubectl apply -f argo-workflow-controller-configmap.yaml --namespace argodev

# To access minio UI - Portforward and access at https://localhost:9000
# kubectl port-forward svc/argo-artifacts 9000:9000 --namespace argodev
