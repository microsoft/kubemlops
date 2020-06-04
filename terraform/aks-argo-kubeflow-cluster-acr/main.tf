module "provider" {
  source = "github.com/microsoft/bedrock/cluster/azure/provider"
}

data "azurerm_resource_group" "resource_group" {
  name = var.resource_group_name
}

resource "azurerm_container_registry" "acr" {
  name                     = var.acr_name
  resource_group_name      = data.azurerm_resource_group.resource_group.name
  location                 = data.azurerm_resource_group.resource_group.location
  sku                      = var.acr_sku
  admin_enabled            = var.acr_admin_enabled
  georeplication_locations = var.acr_georeplication_locations
}

module "vnet" {
  source = "github.com/microsoft/bedrock/cluster/azure/vnet"

  resource_group_name     = data.azurerm_resource_group.resource_group.name
  vnet_name               = var.vnet_name
  address_space           = var.address_space

  tags = {
    environment = "azure-simple"
  }
}

module "subnet" {
  source = "github.com/microsoft/bedrock/cluster/azure/subnet"

  subnet_name          = ["${var.cluster_name}-aks-subnet"]
  vnet_name            = module.vnet.vnet_name
  resource_group_name  = data.azurerm_resource_group.resource_group.name
  address_prefix       = [var.subnet_prefix]
}

module "aks-gitops" {
  source = "github.com/microsoft/bedrock/cluster/azure/aks-gitops"

  acr_enabled              = var.acr_enabled
  agent_vm_count           = var.agent_vm_count
  agent_vm_size            = var.agent_vm_size
  cluster_name             = var.cluster_name
  dns_prefix               = var.dns_prefix
  flux_recreate            = var.flux_recreate
  gc_enabled               = var.gc_enabled
  gitops_ssh_url           = var.gitops_ssh_url
  gitops_ssh_key_path      = var.gitops_ssh_key_path
  gitops_path              = var.gitops_path
  gitops_poll_interval     = var.gitops_poll_interval
  gitops_label             = var.gitops_label
  gitops_url_branch        = var.gitops_url_branch
  ssh_public_key           = var.ssh_public_key
  resource_group_name      = data.azurerm_resource_group.resource_group.name
  service_principal_id     = var.service_principal_id
  service_principal_secret = var.service_principal_secret
  vnet_subnet_id           = tostring(element(module.subnet.subnet_ids, 0))
  service_cidr             = var.service_cidr
  dns_ip                   = var.dns_ip
  docker_cidr              = var.docker_cidr
  network_plugin           = var.network_plugin
  network_policy           = var.network_policy
  oms_agent_enabled        = var.oms_agent_enabled
  kubernetes_version       = var.kubernetes_version
}