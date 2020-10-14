#!/bin/sh


kubectl apply -k github.com/kubeflow/pipelines/manifests/kustomize/cluster-scoped-resources
kubectl wait crd/applications.app.k8s.io --for condition=established --timeout=60s

# Update Argo workflow config to use "pns" containerRuntimeExecutor instead of default "docker"
# to support containerd
# https://github.com/kubeflow/pipelines/issues/1654
# https://github.com/kubeflow/pipelines/issues/1654#issuecomment-595722994
kubectl patch configmap/workflow-controller-configmap -n kubeflow --patch  "$(cat workflow-controller-configmap-patch.yaml)"


### To use default cloud agnostic storages for Kubeflow pipelines metadata, apply the following
    kubectl apply -k github.com/kubeflow/pipelines/manifests/kustomize/env/platform-agnostic

### To backup Kubeflow pipelines metadata with managed Azure services follow the instructions:
### https://github.com/kubeflow/pipelines/blob/master/manifests/kustomize/env/azure/readme.md
### and apply the following:
    kubectl apply -k github.com/kubeflow/pipelines/manifests/kustomize/env/azure


# Apply the Istio resources
kubectl apply -f istio-resources.yaml

