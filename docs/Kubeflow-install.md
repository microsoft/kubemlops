# Kubeflow installation instruction

## Install Istio (if not already installed on the cluster)

(https://istio.io/docs/setup/getting-started/#download)


## Install Kubeflow core + Kubeflow pipelines

* Use [kubeflow-install.sh](../setup/kfp/kubeflow-install.sh) script or follow the manual steps below
* Download the kfctl v1.0.2 release from the [Kubeflow releases page](https://github.com/kubeflow/kfctl/releases/tag/v1.0.2).
* Unpack the tar ball
```
tar -xvf kfctl_v1.0.2_<platform>.tar.gz
```
* Install the package
```
# The following command is optional, to make kfctl binary easier to use.
export PATH=$PATH:<path to where kfctl was unpacked>

# Set KF_NAME to the name of your Kubeflow deployment. This also becomes the
# name of the directory containing your configuration.
# For example, your deployment name can be 'my-kubeflow' or 'kf-test'.
export KF_NAME=<your choice of name for the Kubeflow deployment>

# Set the path to the base directory where you want to store one or more 
# Kubeflow deployments. For example, /opt/.
# Then set the Kubeflow application directory for this deployment.
export BASE_DIR=<path to a base directory>
export KF_DIR=${BASE_DIR}/${KF_NAME}

# Set the configuration file to use, such as the file specified below:
export CONFIG_URI="setup/kfp/kfctl_k8s_light.yaml"

# Generate and deploy Kubeflow:
mkdir -p ${KF_DIR}
cd ${KF_DIR}
kfctl apply -V -f ${CONFIG_URI}
```

## Verify the installation

Wait until pods in the *kubeflow* namespaces are up and running
```
kubectl get pods -n kubeflow
```

## Delete the installation

```
cd ${KF_DIR}
kfctl delete -V -f ${CONFIG_URI}
```

