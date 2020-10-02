data "azurerm_resource_group" "storage" {
  name = var.resource_group_name
}

resource "azurerm_storage_account" "this" {
  name                     = var.storage_name
  resource_group_name      = data.azurerm_resource_group.storage.name
  location                 = data.azurerm_resource_group.storage.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}