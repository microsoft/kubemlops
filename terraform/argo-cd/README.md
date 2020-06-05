# Argo

This Work in Progress Terraform module will install [ArgoCD](https://argoproj.github.io/) on a Kubernetes cluster.

## TODO:
- Investigate namespace. Verified to work with default namespace `argocd`.
- Investigate options for deploying the entire manifest repository as a single argoCD application and its configurations (root, branch, force sync, schedule etc.,)
