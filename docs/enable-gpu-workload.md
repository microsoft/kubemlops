# Enable GPU for Kubeflow Pipelines on Azure Kubernetes Service (AKS)

Graphical processing units (GPUs) are often used for compute-intensive workloads such as graphics and visualization workloads. AKS supports the creation of GPU-enabled node pools to run these compute-intensive workloads in Kubernetes

## Prerequisites

1. **GPU-enabled node pool on AKS** <BR>
To enable GPU on your Kubeflow cluster, follow the [instructions](https://docs.microsoft.com/en-us/azure/aks/gpu-cluster) on how to use GPUs for compute-intensive workloads on Azure Kubernetes  Service (AKS)

For AKS cluster with existing CPU node pool, you can add another node pool with GPUs

```
az aks nodepool add \
    --resource-group myResourceGroup \
    --cluster-name myAKSCluster \
    --node-vm-size Standard_NC6 \
    --name gpu \
    --node-count 3
```

- Create and add [multiple node pools to AKS](https://docs.microsoft.com/en-us/azure/aks/use-multiple-node-pools)<BR>
- See all available [GPU optimized VM size](https://docs.microsoft.com/en-us/azure/virtual-machines/sizes-gpu)

2. **Install NVIDIA drivers**

   Install [NVIDIA drivers](../setup/kfp/nvidia-device-plugin-ds.yaml) in Kubernetes namespace to deploy DaemonSet for the NVIDIA device plugin. This DaemonSet runs a pod on each node to provide the required drivers for the GPUs.

   ``kubectl create namespace gpu-resources`` <br>
   ``kubectl apply -f nvidia-device-plugin-ds.yaml``

## Configure ContainerOp to consume GPUs

Set the node selector constraint on ContainerOp which sets the pod specification of the component to run pod on specific device matching key-value label.

```
import kfp.dsl as dsl
gpu_op = dsl.ContainerOp(name='gpu-op', ...)
gpu_op.add_node_selector_constraint('accelerator', 'nvidia')
```

## Set GPU limit

GPU limit can be set with set_gpu_limit() on ContainerOp.

```
import kfp.dsl as dsl
gpu_op = dsl.ContainerOp(name='gpu-op', ...).set_gpu_limit(2)
```

### Sample component that runs on GPU

This repository has a sample component [(gpu-op)](../code/gpu-op/src/program.py) that runs Pytorch container that checks and print GPU(CUDA) device specification.  
