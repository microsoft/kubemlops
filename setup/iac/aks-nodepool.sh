# For adding GPU-enabled nodepools, see https://github.com/kaizentm/kubemlops/blob/master/docs/enable-gpu-workload.md

# Create a spot instance nodepool
# https://docs.microsoft.com/en-us/azure/aks/spot-node-pool
az aks nodepool add \
    --resource-group $RESOURCE_GROUP \
    --cluster-name $AKS_NAME \
    --name spotnodepool \
    --priority Spot \
    --eviction-policy Delete \
    --spot-max-price -1 \
    --enable-cluster-autoscaler \
    --min-count 1 \
    --max-count 3 \
    --no-wait

az aks nodepool show --cluster-name $AKS_NAME -n spotnodepool -g $RESOURCE_GROUP

# Create a virtual nodepool
# https://docs.microsoft.com/en-us/azure/aks/virtual-nodes-cli
az network vnet subnet create \
    --resource-group $RESOURCE_GROUP-nodepool \
    --vnet-name aks-vnet-15436441 \
    --name acinodepool \
    --address-prefixes 10.241.0.0/16

# az network vnet show --resource-group $RESOURCE_GROUP-nodepool --name aks-vnet-15436441 --query id -o tsv
az role assignment create --assignee <appId> --scope /subscriptions/<subscription>/resourceGroups/kubeflowyo-nodepool/providers/Microsoft.Network/virtualNetworks/aks-vnet-15436441 --role Contributor
az aks enable-addons \
    --resource-group $RESOURCE_GROUP \
    --name $AKS_NAME \
    --addons virtual-node \
    --subnet-name acinodepool

# add regular node pool
az aks nodepool add \
    --resource-group $RESOURCE_GROUP \
    --cluster-name $AKS_NAME \
    --name trainpool2 \
    --enable-cluster-autoscaler \
    --min-count 1 \
    --max-count 3 \
    --no-wait
    --node-vm-size Standard_DS1_v2
