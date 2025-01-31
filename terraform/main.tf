// filepath: summarizer/terraform/main.tf
provider "azurerm" {
  subscription_id = var.subscription_id
  features {}
}

resource "azurerm_resource_group" "summarizer" {
  name     = "summarize-resources"
  location = "West Europe"
}

resource "azurerm_container_registry" "summarizer" {
  name                = "jprosummarizeracr"
  resource_group_name = azurerm_resource_group.summarizer.name
  location            = azurerm_resource_group.summarizer.location
  sku                 = "Basic"
  admin_enabled       = true
}



//  terraform init --upgrade
//  terraform plan -out=tfplan
//  terraform apply tfplan
//  terraform destroy
