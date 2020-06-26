data "azurerm_resource_group" "aksgitops" {
    name = var.resource_group_name
}

module "aks" {
  source = "github.com/microsoft/bedrock/cluster/azure/aks"

  resource_group_name      = data.azurerm_resource_group.aksgitops.name
  cluster_name             = var.cluster_name
  agent_vm_count           = var.agent_vm_count
  agent_vm_size            = var.agent_vm_size
  dns_prefix               = var.dns_prefix
  vnet_subnet_id           = var.vnet_subnet_id
  ssh_public_key           = var.ssh_public_key
  msi_enabled              = var.msi_enabled
  service_principal_id     = var.service_principal_id
  service_principal_secret = var.service_principal_secret
  service_cidr             = var.service_cidr
  dns_ip                   = var.dns_ip
  docker_cidr              = var.docker_cidr
  kubernetes_version       = var.kubernetes_version
  kubeconfig_filename      = var.kubeconfig_filename
  network_policy           = var.network_policy
  network_plugin           = var.network_plugin
  oms_agent_enabled        = var.oms_agent_enabled

  tags = var.tags
}

module "argo_cd" {
  source = "../../common/argo-cd"

  argo_cd_repo             = var.argo_cd_repo
  argo_cd_namespace        = var.argo_cd_namespace
  argo_cd_recreate         = var.argo_cd_recreate
  enable_argo_cd           = var.enable_argo_cd

  gitops_ssh_key_path      = var.gitops_ssh_key_path
  kubeconfig_complete      = module.aks.kubeconfig_done
  kubeconfig_filename      = var.kubeconfig_filename
}
