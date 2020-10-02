# Note: These terraform scripts require the service principal or user to already be logged in with
# az login before running the scripts!
#
# Example:
# az login
# az account set -s <subscription to deploy>

provider "azurerm" {
  features {}
  skip_provider_registration = true
}

data "azurerm_subscription" "current" {}
data "azurerm_client_config" "current" {}

data "azurerm_resource_group" "this" {
  name = var.resource_group_name
}
