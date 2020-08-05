# Kubeflow installation instruction

## Connect to AKS

* Login to Azure: `az login`
* Create user credentials:  `az aks get-credentials -n <AKS_NAME> -g <RESOURCE_GROUP_NAME>`

## Install Istio (if not already installed on the cluster)

(https://istio.io/docs/setup/getting-started/#download)


## Install Kubeflow core + Kubeflow pipelines

* Use [kubeflow-install.sh](../setup/kfp/kubeflow-install.sh) script

## Verify the installation

Wait until pods in the *kubeflow* namespaces are up and running
```
kubectl get pods -n kubeflow
```

