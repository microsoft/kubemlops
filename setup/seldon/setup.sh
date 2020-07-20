kubectl create namespace seldon-system

# Need to create seldon crd explicitly (not with a helm chart)
# due to incompatibility issue with K8s v1.18
# https://github.com/SeldonIO/seldon-core/issues/1675

kubectl apply -f seldon-crd.yaml -n seldon-system

helm install seldon-core seldon-core-operator --repo https://storage.googleapis.com/seldon-charts --set istio.enabled=true --set usageMetrics.enabled=true --set crd.create=false --namespace seldon-system

kubectl apply -f gateway.yaml