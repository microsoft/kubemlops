module "common-provider" {
  source = "../provider"
}

resource "null_resource" "deploy_argo_cd" {
  count = var.enable_argo_cd ? 1 : 0

  provisioner "local-exec" {
    command = "echo 'Need to use this var so terraform waits for kubeconfig ' ${var.kubeconfig_complete};KUBECONFIG=${var.output_directory}/${var.kubeconfig_filename} ${path.module}/deploy_argocd.sh -n '${var.argo_cd_namespace}' -r '${var.argo_cd_repo}' -s '${var.gitops_ssh_key_path}'"
  }

  triggers = {
    enable_argo_cd   = var.enable_argo_cd
    argo_cd_recreate = var.argo_cd_recreate
  }
}
