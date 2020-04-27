# https://argoproj.github.io/docs/argo/getting-started.html
wget https://github.com/argoproj/argo/releases/download/v2.7.5/argo-linux-amd64 -O ~/tmp/argo
chmod +x ~/tmp/argo
sudo mv ~/tmp/argo /usr/local/bin

kubectl create namespace argodev
kubens argodev
kubectl apply -f https://raw.githubusercontent.com/argoproj/argo/stable/manifests/install.yaml
kubectl create rolebinding default-admin --clusterrole=admin --serviceaccount=default:default

helm install argo-artifacts stable/minio \
  --set service.type=ClusterIP \
  --set defaultBucket.enabled=true \
  --set defaultBucket.name=my-bucket \
  --set persistence.enabled=false \
  --set fullnameOverride=argo-artifacts

k port-forward svc/argo-artifacts 9000:9000

k apply -f argo-workflow-controller-configmap.yaml
