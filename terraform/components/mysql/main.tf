data "azurerm_resource_group" "mysql" {
  name = var.resource_group_name
}

resource "azurerm_mysql_server" "this" {
  name                = var.mysql_name
  location            = data.azurerm_resource_group.mysql.location
  resource_group_name = data.azurerm_resource_group.mysql.name

  administrator_login          = "kfpsqladminun"
  administrator_login_password = var.mysql_admin_pass

  sku_name   = "GP_Gen5_2"
  storage_mb = 5120
  version    = "5.7"

  auto_grow_enabled                 = true
  backup_retention_days             = 7
  geo_redundant_backup_enabled      = true
  infrastructure_encryption_enabled = true
  public_network_access_enabled     = true
  ssl_enforcement_enabled           = false
}
