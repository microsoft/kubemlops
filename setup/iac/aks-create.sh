# One-time pre-requisite setup per subscription
# https://docs.microsoft.com/en-us/azure/aks/cluster-configuration
# https://docs.microsoft.com/en-us/azure/aks/spot-node-pool
# az feature register --name UseCustomizedContainerRuntime --namespace Microsoft.ContainerService
# az feature register --name Gen2VMPreview --namespace Microsoft.ContainerService
# az feature register --name spotpoolpreview --namespace Microsoft.ContainerService
# Will have to wait minutes for registration to complete then run this
# az provider register --namespace Microsoft.ContainerService

az extension add --name aks-preview

az aks create -n $AKS_NAME -g $RESOURCE_GROUP -l $LOCATION \
  --kubernetes-version $K8S_VERSION \
  --node-count $NODE_COUNT \
  --vm-set-type VirtualMachineScaleSets \
  --load-balancer-sku standard \
  --enable-cluster-autoscaler \
  --min-count 1 \
  --max-count 3 \
  --dns-name-prefix $AKS_NAME \
  --node-vm-size $VM_SIZE \
  --enable-managed-identity \
  --network-plugin azure \
  --generate-ssh-keys \
  --service-principal $AKS_SERVICE_PRICIPAL \
  --client-secret $AKS_SERVICE_PRINCIPAL_SECRET \
  --node-resource-group $AKS_NAME-nodepool \
  --aks-custom-headers usegen2vm=true,ContainerRuntime=containerd
