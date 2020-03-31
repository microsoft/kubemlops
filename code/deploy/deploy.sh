# az ml model deploy -n tacosandburritos -m tacosandburritos:1 --ic inferenceconfig.json --dc deploymentconfig.json --resource-group taco-rg --workspace-name taco-workspace --overwrite -v
#!/bin/sh
while getopts "m:n:i:d:s:p:u:r:w:t:b:x:" option;
    do
    case "$option" in
        m ) MODEL=${OPTARG};;
        n ) MODEL_NAME=${OPTARG};;
        i ) INFERENCE_CONFIG=${OPTARG};;
        d ) DEPLOYMENTCONFIG=${OPTARG};;
        s ) SERVICE_PRINCIPAL_ID=${OPTARG};;
        p ) SERVICE_PRINCIPAL_PASSWORD=${OPTARG};;
        u ) SUBSCRIPTION_ID=${OPTARG};;
        r ) RESOURCE_GROUP=${OPTARG};;
        w ) WORKSPACE=${OPTARG};;
        t ) TENANT_ID=${OPTARG};;
        b ) BASE_PATH=${OPTARG};;
        x ) RUN_ID=${OPTARG};;
    esac
done
az login --service-principal --username ${SERVICE_PRINCIPAL_ID} --password ${SERVICE_PRINCIPAL_PASSWORD} -t $TENANT_ID
# az ml model deploy -n $MODEL_NAME -m ${MODEL}:1 --ic $INFERENCE_CONFIG --pi ${BASE_PATH}/myprofileresult.json --dc $DEPLOYMENTCONFIG -w $WORKSPACE -g $RESOURCE_GROUP --overwrite -v
# model_id=$(az ml model list --model-name $MODEL --workspace-name $WORKSPACE -g $RESOURCE_GROUP --tag run_id=$RUN_ID | jq '.[0] | .id') 
echo $MODEL
echo $WORKSPACE
echo $RESOURCE_GROUP
echo $SUBSCRIPTION_ID
model_id=$(az ml model list --model-name $MODEL --workspace-name $WORKSPACE -g $RESOURCE_GROUP --subscription-id $SUBSCRIPTION_ID --tag run_id=$RUN_ID | jq -r '.[0] | .id') 
echo $model_id

az ml model deploy -n "mexicanfood" -m $model_id --ic $INFERENCE_CONFIG  --dc $DEPLOYMENTCONFIG -w $WORKSPACE -g $RESOURCE_GROUP --overwrite -v
