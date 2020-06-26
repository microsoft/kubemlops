kubectl create namespace argo
kubectl apply -n argo -f https://raw.githubusercontent.com/argoproj/argo/stable/manifests/install.yaml

# grant the default ServiceAccount admin privileges (i.e., binds the admin role to the default ServiceAccount of the argo namespace):
kubectl create rolebinding default-admin --clusterrole=admin --serviceaccount=argo:default -n argo

# Note that this will grant admin privileges to the default ServiceAccount in the given namespace for the command;
# so you will only be able to run Workflows in the namespace where the RoleBinding was made.

# optional: install minio as artifact storage
helm install argo-artifacts stable/minio --namespace argo --set service.type=ClusterIP --set defaultBucket.enabled=true --set defaultBucket.name=my-bucket --set persistence.enabled=false --set fullnameOverride=argo-artifacts

# Run coinflip workflow
argo submit -n argo --watch https://raw.githubusercontent.com/argoproj/argo/master/examples/coinflip.yaml
