# Create the resources required to set up the kubeflow installation
# with perpetuated resources (mysql/minio) hosted on Azure services.

az extension add --name db-up

az mysql up --server-name $MYSQL_NAME \
--admin-user $MYSQL_USER \
--admin-password $MYSQL_PASS \
--location $LOCATION \
--resource-group $RESOURCE_GROUP \
--ssl-enforcement Disabled

az storage account create \
--name $STORAGE_NAME \
--resource-group $RESOURCE_GROUP \
--location $LOCATION \
--sku Standard_ZRS \
--encryption-services blob
