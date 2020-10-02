variable "resource_group_name" {
  type = string
}

variable "kubernetes_version" {
  type = string
}

variable "location" {
  type = string
  default = ""
}

variable "cluster_name" {
  type = string
}

variable "dns_prefix" {
  type = string
}

variable "vm_count" {
  description = "count of VMs in default node pool"
  type = string
}

variable "vm_size" {
  description = "size of VMs in default node pool"
  type = string
}

variable "os_disk_size_gb" {
  type = string
}

variable "acr_id" {
  description = "id of acr associated with the cluster"
  type = string
}

variable "vnet_subnet_id" {
  description = "The subnet id of the virtual network."
  type = string
}

variable "tags" {
  description = "The tags to associate with AKS"
  type        = map

  default = {}
}

variable "kubeconfig_to_disk" {
  description = "For local testing - write kubeconfig file to local disk"
  type = bool
  default = false
}

variable "output_directory" {
  type      =   string
  default   =   "./output"
}

variable "kubeconfig_filename" {
  description = "Name of the kube config file saved to disk."
  type        = string
  default     = "onepoint_kube_config"
}