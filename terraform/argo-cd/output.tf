output "argo_cd_done" {
  value = join("",null_resource.deploy_argo_cd.*.id)
}
