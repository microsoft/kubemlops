# AKS with ArgoCD

This Terraform module is based on the [Bedrock](https://github.com/microsoft/bedrock) project's [aks-gitops](https://github.com/microsoft/bedrock/tree/master/cluster/azure/aks-gitops) module. Instead of installing flux as the GitOps sync tool, it will install the [argo-cd](../../common/argo-cd/README.md) module.
