variable "location" {
  default     = "West US 2"
  type        = string
  description = "Location to deploy resource group and resources"
}

variable "resource_group_name" {
  type        = string
  description = "Name of resource group to deploy to"
}

variable "default_nodepool_vm_size" {
  type        = string
  default     = "Standard_D2_v2"
  description = "Size of nodes in default nodepool"
}

variable "default_node_count" {
  type = string
  default = 1
  description = "Number of nodes in default nodepool"
}

variable "os_disk_size_gb" {
  type = string
  default = 32
}

variable "container_registry_sku" {
  type = string
  default = "Standard"
}

variable "container_registry_name" {
  type = string
}

variable "cluster_name" {
  type = string
}

variable "aks_address_space" {
  type = string
  default = "172.53.0.0/16"
}

variable "aks_subnet_prefix" {
  type = string
  default = "172.53.0.0/21"
}

variable "virtual_network_name" {
  type = string
  default = "kf_vnet"
}

variable "subnet_name" {
  type = string
  default = "kf_subnet"
}

variable "kubernetes_version" {
  type    = string
  default = "1.17.11"
}

variable "mysql_name" {
  type    = string
  default = "kfp-mysql"
  description = "name of mysql server"
}

variable "mysql_admin_pass" {
  type    = string
  description = "password for mysql admin user"
}

variable "storage_name" {
  type    = string
  default = "kfpminio"
  description = "name for storage account"
}