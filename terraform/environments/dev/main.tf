resource "azurerm_resource_group" "rg" {
  name     = "rg-ai-terraform-reviewer-dev"
  location = "East US"
}

module "shared_network" {
  source              = "../../modules/network"
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location

  vnet_name     = "vnet-shared-dev"
  address_space = ["10.0.0.0/16"]

  subnets = {
    shared-subnet = {
      address_prefixes = ["10.0.1.0/24"]
    }
    app-subnet-v2 = {
      address_prefixes = ["10.0.2.0/24"]
    }
  }
}
