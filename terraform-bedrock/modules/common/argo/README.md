# Argo

This Work in Progress Terraform module will install [Argo](https://argoproj.github.io/) on a Kubernetes cluster along with a [MinIO](https://min.io/) server.

This module currently has issues with clusterroles. Argo is unable to call any kubernetes apis.

## TODO:
- [RBAC](https://argoproj.github.io/docs/argo/workflow-rbac.html) for argo service account.
- Investigate MinIO artifact buckets
- Setting MinIO default access and secret keys
- [Sample workflows](https://argoproj.github.io/docs/argo/getting-started.html#4-run-sample-workflows)
