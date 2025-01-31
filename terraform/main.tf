// filepath: summarizer/terraform/main.tf
provider "azurerm" {
  subscription_id = var.subscription_id
  features {}
}

resource "azurerm_resource_group" "summarizer" {
  name     = "jpro-summarize-resources"
  location = "Norway East"
}

data "azurerm_client_config" "current" {}

locals {
  current_user_id = coalesce(var.msi_id, data.azurerm_client_config.current.object_id)
}

resource "azurerm_container_registry" "summarizer" {
  name                = "jprosummarizeracr"
  resource_group_name = azurerm_resource_group.summarizer.name
  location            = azurerm_resource_group.summarizer.location
  sku                 = "Basic"
  admin_enabled       = true
}

resource "azurerm_key_vault" "summarizer" {
  name                        = "jprosummarizerkv"
  location                    = azurerm_resource_group.summarizer.location
  resource_group_name         = azurerm_resource_group.summarizer.name
  sku_name                    = "standard"
  tenant_id                   = data.azurerm_client_config.current.tenant_id
  soft_delete_retention_days  = 7

  access_policy {
    tenant_id = data.azurerm_client_config.current.tenant_id
    object_id = local.current_user_id
  }
}


//  terraform init --upgrade
//  terraform plan -out=tfplan
//  terraform apply tfplan
//  terraform destroy
