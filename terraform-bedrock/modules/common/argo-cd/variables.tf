# A repository to configure Argo to point to, more can be added later
variable "argo_cd_repo" {
  description = "ssh git clone repository URL with Kubernetes manifests including services which runs in the cluster. ArgoCD monitors this repo resources and changes to sync them to the cluster."
  type        = string
}

# Default ArgoCD namespace
variable "argo_cd_namespace" {
  type    = string
  default = "argocd"
}

# generate a SSH key named identity: ssh-keygen -q -N "" -f ./identity
# or use existing ssh public/private key pair
# add deploy key in gitops repo using public key with read/write access
# assign/specify private key to "gitops_ssh_key_path" variable that will be used to cretae kubernetes secret object
# flux use this key to read manifests in the git repo
variable "gitops_ssh_key_path" {
  type = string
}

variable "output_directory" {
  type    = string
  default = "./output"
}

variable "enable_argo_cd" {
  type    = string
  default = "true"
}

variable "kubeconfig_filename" {
  description = "Name of the kube config file saved to disk."
  type        = string
  default     = "bedrock_kube_config"
}

variable "argo_cd_recreate" {
  description = "Make any change to this value to trigger the recreation of the argo-cd execution script."
  type        = string
  default     = ""
}

variable "kubeconfig_complete" {
  description = "Allows flux to wait for the kubeconfig completion write to disk. Workaround for the fact that modules themselves cannot have dependencies."
  type        = string
}
