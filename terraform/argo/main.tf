module "common-provider" {
  source = "github.com/microsoft/bedrock/cluster/common/provider"
}

resource "null_resource" "deploy_argo" {
  count = var.enable_argo ? 1 : 0

  provisioner "local-exec" {
    command = "echo 'Need to use this var so terraform waits for kubeconfig ' ${var.kubeconfig_complete};KUBECONFIG=${var.output_directory}/${var.kubeconfig_filename} ${path.module}/deploy_argo.sh"
  }

  triggers = {
    enable_argo   = var.enable_argo
    argo_recreate = var.argo_recreate
  }
}
