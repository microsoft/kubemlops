# Terraform template for Kubeflow backed by Azure

This template provides a basic cluster setup in an existing Azure resource group for Kubeflow or Kubeflow Pipelines using Terraform 0.12 [(download](https://releases.hashicorp.com/terraform/0.12.28/)).

* AKS cluster
* Azure Container Registry (to store Kubeflow component containers)
* MySQL (used by Pipelines and Metadata)
* Storage (used by Minio Gateway for Blobstore)

## Usage

1. Log in to your subscription

    ``` bash
    az login
    ```

1. Select an existing resource group or create a new resource group

1. [Optional] Create terraform.tfvars file to specify variable values

    See [variables.tf](variables.tf) for required and optional variables

1. Apply the template

    ``` bash
    terraform init
    terraform plan
    terraform apply
    ```
