docker build . -t kubeflowyoacr.azurecr.io/seldon-pipeline:latest

docker push kubeflowyoacr.azurecr.io/seldon-pipeline:latest

kubectl apply -f pipeline.yaml  -n serving
