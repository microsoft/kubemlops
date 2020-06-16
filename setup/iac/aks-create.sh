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
  --generate-ssh-keys
  
