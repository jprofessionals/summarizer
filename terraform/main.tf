// filepath: summarizer/terraform/main.tf
provider "azurerm" {
  features {}
}

resource "azurerm_resource_group" "summarizer" {
  name     = "example-resources"
  location = "West Europe"
}

resource "azurerm_container_registry" "summarizer" {
  name                = "summarizeracr"
  resource_group_name = azurerm_resource_group.summarizer.name
  location            = azurerm_resource_group.summarizer.location
  sku                 = "Basic"
  admin_enabled       = true
}

output "acr_login_server" {
  value = azurerm_container_registry.summarizer.login_server
}

output "acr_admin_username" {
  value = azurerm_container_registry.summarizer.admin_username
}

output "acr_admin_password" {
  value = azurerm_container_registry.summarizer.admin_password
}
