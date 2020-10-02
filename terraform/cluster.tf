module "acr" {
    source = "./components/acr"

    name                = var.container_registry_name
    resource_group_name = var.resource_group_name
    sku                 = var.container_registry_sku
}

module "aks_vnet" {
    source = "./components/vnet"
    
    resource_group_name = var.resource_group_name
    vnet_name           = var.virtual_network_name
    address_space       = var.aks_address_space
}

module "aks_subnet" {
  source = "./components/subnet"

  subnet_name         = var.subnet_name
  resource_group_name = var.resource_group_name
  vnet_name           = module.aks_vnet.vnet_name
  address_prefixes    = [var.aks_subnet_prefix]
  service_endpoints   = ["Microsoft.Sql", "Microsoft.Storage"]
}

module "aks_cluster" {
    source = "./components/aks"

    resource_group_name = var.resource_group_name
    location            = var.location
    cluster_name        = var.cluster_name
    dns_prefix          = var.cluster_name
    vm_size             = var.default_nodepool_vm_size
    vm_count            = var.default_node_count
    os_disk_size_gb     = var.os_disk_size_gb
    acr_id              = "${module.acr.acr_id}"
    vnet_subnet_id      = "${module.aks_subnet.subnet_id}"
    kubernetes_version  = var.kubernetes_version
}

module "mysql" {
  source = "./components/mysql"

  resource_group_name = var.resource_group_name
  mysql_name          = var.mysql_name
  mysql_admin_pass    = var.mysql_admin_pass
}

resource "azurerm_mysql_virtual_network_rule" "example" {
  name                = "mysql-vnet-rule"
  resource_group_name = var.resource_group_name
  server_name         = module.mysql.mysql_name
  subnet_id           = module.aks_subnet.subnet_id
}

module "storage" {
  source = "./components/storage"

  resource_group_name = var.resource_group_name
  storage_name        = var.storage_name
}