#!/bin/bash

export DATABRICKS_HOST='YOUR Domain '
export DATABRICKS_TOKEN='SECRET'

echo $DATABRICKS_HOST
echo $DATABRICKS_TOKEN
echo 'Login to Databricks CLI'

# databricks configure --token << ANSWERS
# $DATABRICKS_HOST
# $DATABRICKS_TOKEN
# ANSWERS

databricks workspace

export MLFLOW_TRACKING_URI=databricks
mlflow run . -e main --experiment-id 1315550910283717 -b databricks --backend-config clusterconfig.json