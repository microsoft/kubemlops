# Securing Kubeflow on AKS

* Run [azure-credentials.sh](../setup/kfp/azure-credentials.sh)
  * This file sets Azure service principal secrets in the AKS cluster. Initialize variables in the script before running it.
* Run [ghcreds-secret.sh](../setup/kfp/ghcreds-secret.sh)
  * This file set Git access token secrets in the AKS cluster. Initialize variables in the script before running it.
* Run [kubemlopsbot.sh](../setup/kfp/kubemlopsbot.sh)
  * Manually installs a k8s deployment for a custom bot. Initialize variables in the script before running it.
* Run [pvc.sh](../setup/kfp/pvc.sh)
  * Deploy a PVC configuration in kubeflow namespace
* Run [attach-acr.sh](../setup/kfp/attach-acr.sh). Initialize variables in the script before running it.
  * Use Az CLI to authenticate Azure Container Registry with AKS