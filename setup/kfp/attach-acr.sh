# Initialize variables:
# AKS_NAME=
# RESOURCE_GROUP=
# ACR_NAME=

az aks update -n $AKS_NAME -g $RESOURCE_GROUP --attach-acr $ACR_NAME