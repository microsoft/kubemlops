# Terraform template deployment

This is a Work in Progress template for deploying:

1. A single Azure Container Registry with geo replication
2. A single Azure Kubernetes Service Cluster and supporting infrastructure
3. Currently Flux is also deployed to the above AKS cluster
4. WIP - [Argo](https://github.com/argoproj/argo) deployment on cluster
   1. [MinIO](https://min.io/) server for supporting ArgoCD
5. WIP - [ArgoCD](https://github.com/argoproj/argo-cd) deployment on cluster

These templates are leaning heavily on [Bedrock](https://github.com/microsoft/bedrock) terraform [templates](https://github.com/microsoft/bedrock/tree/master/cluster). 

Additionally, these templates will only deploy to an existing Azure Resource Group. This practice prevents Terraform from destroying any other resources that may be added to a Terraform created Resource Group in the future.

## Requirements:
- [Azure CLI](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli?view=azure-cli-latest)
  - **MacOS**:
    - via homebrew: `brew update && brew install azure-cli`
- [Terraform v12)](https://www.terraform.io/downloads.html)
  - **Linux**:
    - via snap: `snap install kubectl --classic` - May be out of date, will only install Terraform v11.11
    - Manually steps for installing the latest: https://askubuntu.com/a/983352
  - **MacOS**:
    - via homebrew: `brew install terraform`
- [kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/)
  - **Linux**:
    - via snap: `snap install kubectl --classic`
  - **MacOS**:
    - via homebrew: `brew install kubectl`
- [Helm v3](https://helm.sh/) - install scripts _should_ download.
- TBD: [ArgoCD CLI](https://argoproj.github.io/argo-cd/cli_installation/)
  - **MacOS**:
    - via homebrew: `brew tap argoproj/tap && brew install argoproj/tap/argocd`
- TBD: [Argo CLI](https://github.com/argoproj/argo/releases)

## Steps for deployment:
- Az Login
- Create Service Principal
- Create SSH key for cluster/git repository persmissions
- Configure `.tfvars` file
- `terraform init`
- `terraform plan -var-file *.tfvars`
- `terraform apply -var-file *.tfvars`

## Argo Sample Workoflows:
https://argoproj.github.io/docs/argo/getting-started.html#4-run-sample-workflows

## ArgoCD Sample Workflows:
https://github.com/argoproj/argocd-example-apps

## Sample workflow with Argo & ArgoCD:
https://github.com/SeldonIO/seldon-core/tree/master/examples/cicd/cicd-argocd

## TODOs
- Link Argo module
  - Optionally, add flag to disable/skip this module
- Link ArgoCD module
  - Optionally, add flag to disable/skip this module
- Clean up tf varabile files
- Clean up sample .tfvars files
- TBD: unlink/disable flux
- TBD: Explore KubeFlow
- TBD: Explore MLFlow
- TBD: default Istio configuration through terraform module OR fabrikate component
