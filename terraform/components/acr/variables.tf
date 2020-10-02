variable "resource_group_name" {
  type = string
}

variable "name" {
  type = string
}

variable "sku" {
    type = string
}

variable "tags" {
  description = "The tags to associate with ACR"
  type        = map

  default = {}
}