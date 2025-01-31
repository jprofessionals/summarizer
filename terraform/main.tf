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
  envs = { for tuple in regexall("(.*)=(.*)", file("../.env")) : tuple[0] => sensitive(tuple[1]) }
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
  tenant_id                   = data.azurerm_client_config.current.tenant_id
  sku_name                    = "standard"
  soft_delete_retention_days  = 7

  access_policy {
    tenant_id = data.azurerm_client_config.current.tenant_id
    object_id = local.current_user_id

      // Add these lines to grant permissions
    secret_permissions = [
      "Get",
      "List",
      "Set",
      "Delete",
      "Backup",
      "Restore",
      "Recover",
      "Purge"
    ]
  }
}

resource "azurerm_key_vault_secret" "openai_api_key" {
  name         = "OpenAI-API-Key"
  value        = local.envs["OPENAI_API_KEY"]
  key_vault_id = azurerm_key_vault.summarizer.id
}

resource "azurerm_container_group" "summarizer" {
  name                = "jpro-summarizer-container-group"
  location            = azurerm_resource_group.summarizer.location
  resource_group_name = azurerm_resource_group.summarizer.name
  os_type             = "Linux"

  container {
    name   = "summarizer"
    image  = "${azurerm_container_registry.summarizer.login_server}/summarizer-app:latest"
    cpu    = "1.0"
    memory = "1.5"

    ports {
      port     = 80
      protocol = "TCP"
    }

    environment_variables = {
      "ENV_VAR_NAME" = "value"
    }

    secure_environment_variables = {
      "OPENAI_API_KEY" = azurerm_key_vault_secret.openai_api_key.value
    }
  }

  image_registry_credential {
    server   = azurerm_container_registry.summarizer.login_server
    username = azurerm_container_registry.summarizer.admin_username
    password = azurerm_container_registry.summarizer.admin_password
  }

  tags = {
    environment = "testing"
  }
}

//  terraform init --upgrade
//  terraform plan -out=tfplan
//  terraform apply tfplan
//  terraform destroy
