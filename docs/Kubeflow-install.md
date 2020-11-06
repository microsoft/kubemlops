# Kubeflow installation instruction

## Connect to AKS

* Login to Azure: `az login`
* Create user credentials:  `az aks get-credentials -n <AKS_NAME> -g <RESOURCE_GROUP_NAME>`

## Option 1: Install Standalone Kubeflow pipelines

### Install Istio (if not already installed on the cluster)

(https://istio.io/docs/setup/getting-started/#download)

### Install Kubeflow pipelines

* Use [kubeflow-install.sh](../setup/kfp/kubeflow-install.sh) script

### Enable Authentication

* Follow [instructions on enabling Oath 2.0 JWT for Kubeflow](./AuthWIthAzure.md)

## Option 2: Install Kubeflow (https://www.kubeflow.org/docs/azure/deploy/install-kubeflow/)

## Option 3: Install Kubeflow with Authentication (https://www.kubeflow.org/docs/azure/authentication-oidc/)

## Verify the installation

Wait until pods in the *kubeflow* namespaces are up and running
```
kubectl get pods -n kubeflow
```

