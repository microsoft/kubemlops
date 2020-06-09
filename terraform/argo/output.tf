output "argo_done" {
  value = join("",null_resource.deploy_argo.*.id)
}
