#!/bin/bash
while getopts "r:" option;
    do
    case "$option" in
        r ) REGISTRY_NAME=${OPTARG};;
    esac
done
cp -R ../ml_logging ml_logging
IMAGE=${REGISTRY_NAME}.azurecr.io/mlflowproject
docker build -t $IMAGE . && docker run -it $IMAGE
