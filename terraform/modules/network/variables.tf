variable "resource_group_name" {
  type        = string
  description = "Resource group name"
}

variable "location" {
  type        = string
  description = "Azure region"
}

variable "vnet_name" {
  type        = string
  description = "VNet name"
}

variable "address_space" {
  type        = list(string)
}

variable "subnets" {
  description = "Map of subnets"
  type = map(object({
    address_prefixes = list(string)
  }))
}
