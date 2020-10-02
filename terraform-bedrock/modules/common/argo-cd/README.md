# ArgoCD
This Terraform module will install [ArgoCD](https://argoproj.github.io/argo-cd/) on a Kubernetes cluster as well as add a single repository via the argoCD CLI.

## Managing ArgoCD
To access the ArgoCD instance, you must either portforward the `argocd-server` pod or service, _or_ you can expose the service publically with a LoadBalancer.

To portforward the service, run: `kubectl port-forward svc/argocd-server -n argocd 8080:443` and login either via:

- CLI: run `argocd login`
  - The password can be modified via the argoCD CLI after logging in via `argocd account update-password`.
- UI: open a browser to https://localhost:8080

To login via the UI or CLI, the default username is: `admin` and the password is the name of the `argocd-server` pod, eg. `argocd-server-565b7b7d12-abcde`. You can also run this command as a shortcut: `kubectl get pods -n argocd -l app.kubernetes.io/name=argocd-server -o name | cut -d'/' -f 2`.

## Running the script outside of Terraform:
Assuming `kubectl` is already configured to a kubernetes instance, run:

`sh deploy_argocd.sh -n <desired-namespace> -r <repository-git-url> -s <full-path-to-private-ssh-key-file>`

## TODO:
- Investigate namespace. Verified to work with default namespace: `argocd`.
- Investigate options for deploying the entire manifest repository as a single argoCD application and its configurations (root, branch, force sync, schedule etc.)
