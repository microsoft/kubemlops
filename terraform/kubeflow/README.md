# Terraform template deployment

This is a Work in Progress template for deploying:

1. A single Azure Container Registry with geo replication
2. A single Azure Kubernetes Service Cluster and supporting infrastructure
3. Currently Flux is also deployed to the above AKS cluster
4. WIP - [ArgoCd](https://github.com/argoproj/argo-cd) deployment on cluster

These templates are leaning heavily on [Bedrock](https://github.com/microsoft/bedrock) terraform [templates](https://github.com/microsoft/bedrock/tree/master/cluster). 

Additionally, these templates will only deploy to an existing Azure Resource Group. This practice prevents terraform from destroying any other resources that may be added to a Terraform created Resource Group in the future.

## Requirements:
- [Azure CLI](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli?view=azure-cli-latest)
- [Terraform v12)](https://www.terraform.io/downloads.html)
- [kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/)
- TBD: [Argo CLI](https://argoproj.github.io/argo-cd/cli_installation/)

## Steps for deployment:
- Az Login
- Create Service Principal
- Create SSH key for cluster/git repository persmissions
- Configure `.tfvars` file
- `terraform init`
- `terraform plan -var-file *.tfvars`
- `terraform apply -var-file *.tfvars`
