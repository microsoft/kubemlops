# Install the Secret Store csi driver provider
helm repo add csi-secrets-store-provider-azure https://raw.githubusercontent.com/Azure/secrets-store-csi-driver-provider-azure/master/charts
helm install csi-secrets-store-provider-azure/csi-secrets-store-provider-azure --generate-name

# Initialize variables:
# AZ_SUBSCRIPTION_ID=
# AZ_RESOURCE_GROUP=
# AZ_CLIENT_ID=
# AZ_KEYVAULT=
# KUBEFLOW_NAMESPACE=kubeflow

# Give SP Reader access to Keyvault
az role assignment create --role Reader --assignee $AZ_CLIENT_ID --scope /subscriptions/$AZ_SUBSCRIPTION_ID/resourcegroups/$AZ_RESOURCE_GROUP/providers/Microsoft.KeyVault/vaults/$AZ_KEYVAULT

# Create access policy to give SP secret read permission
az keyvault set-policy -n $AZ_KEYVAULT --secret-permissions get --spn $AZ_CLIENT_ID

# Apply secret provider class
kubectl apply -f azsecretprovider.yaml -n $KUBEFLOW_NAMESPACE