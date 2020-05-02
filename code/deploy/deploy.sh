#!/bin/sh
while getopts "m:u:r:w:x:d:" option;
    do
    case "$option" in
        m ) MODEL=${OPTARG};;
        u ) SUBSCRIPTION_ID=${OPTARG};;
        r ) RESOURCE_GROUP=${OPTARG};;
        w ) WORKSPACE=${OPTARG};;
        x ) RUN_ID=${OPTARG};;
        d ) DEPLOYMENT_NAME=${OPTARG};;
    esac
done
echo $MODEL
echo $WORKSPACE
echo $RESOURCE_GROUP
echo $SUBSCRIPTION_ID
echo $RUN_ID
echo $DEPLOYMENT_NAME
az extension add -n azure-cli-ml
model_id=$(az ml model list --model-name $MODEL --workspace-name $WORKSPACE -g $RESOURCE_GROUP --subscription-id $SUBSCRIPTION_ID --tag run_id=$RUN_ID | jq -r '.[0] | .id') 
echo $model_id
az ml model deploy -n $DEPLOYMENT_NAME -m $model_id --ic $GITHUB_WORKSPACE/code/deploy/inferenceconfig.json  --dc $GITHUB_WORKSPACE/code/deploy/deploymentconfig.json -w $WORKSPACE -g $RESOURCE_GROUP --overwrite -v

