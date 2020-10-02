data "azurerm_resource_group" "cluster" {
  name = var.resource_group_name
}

resource "random_id" "workspace" {
  keepers = {
    group_name = data.azurerm_resource_group.cluster.name
  }

  byte_length = 8
}

resource "azurerm_log_analytics_workspace" "workspace" {
  name                = "${data.azurerm_resource_group.cluster.name}-${random_id.workspace.hex}"
  location            = var.location == "" ? data.azurerm_resource_group.cluster.location : var.location
  resource_group_name = data.azurerm_resource_group.cluster.name
  sku                 = "PerGB2018"

  tags = var.tags
}

resource "azurerm_log_analytics_solution" "solution" {
  solution_name         = "ContainerInsights"
  location              = var.location == "" ? data.azurerm_resource_group.cluster.location : var.location
  resource_group_name   = data.azurerm_resource_group.cluster.name
  workspace_resource_id = azurerm_log_analytics_workspace.workspace.id
  workspace_name        = azurerm_log_analytics_workspace.workspace.name

  plan {
    publisher = "Microsoft"
    product   = "OMSGallery/ContainerInsights"
  }
}

resource "azurerm_kubernetes_cluster" "cluster" {
  name                = var.cluster_name
  location            = var.location == "" ? data.azurerm_resource_group.cluster.location : var.location
  resource_group_name = data.azurerm_resource_group.cluster.name
  dns_prefix          = var.dns_prefix
  kubernetes_version  = var.kubernetes_version

  network_profile {
    network_plugin     = "azure"
    network_policy     = "azure"
  }
  
  default_node_pool {
    name            = "default"
    node_count      = var.vm_count
    vm_size         = var.vm_size
    os_disk_size_gb = var.os_disk_size_gb
    type            = "VirtualMachineScaleSets"
    vnet_subnet_id  = var.vnet_subnet_id
  }

  role_based_access_control {
    enabled = true
  }

  identity {
    type = "SystemAssigned"
  }

  tags = var.tags
}

data "azurerm_user_assigned_identity" "aks" {
  name                = "${var.cluster_name}-agentpool"
  resource_group_name = azurerm_kubernetes_cluster.cluster.node_resource_group
}

resource "azurerm_role_assignment" "acrpull_role" {
  scope                            = var.acr_id
  role_definition_name             = "AcrPull"
  principal_id                     = data.azurerm_user_assigned_identity.aks.principal_id
  skip_service_principal_aad_check = true
}