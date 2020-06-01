# https://hub.kubeapps.com/charts/larribas/mlflow

#install postgresql
# if upgrading postgresql, set the postgresqlPassword 
helm repo add bitnami https://charts.bitnami.com/bitnami
helm install postgresql bitnami/postgresql --set metrics.enabled=true --set postgresqlDatabase=mlflow

helm repo add larribas https://larribas.me/helm-charts
helm install mlflow larribas/mlflow --set image.repository="dtzar/mlflow",image.tag="latest",extraArgs.expose-prometheus="yes"

# Access the UI
k port-forward svc/mlflow 5000:5000
http://localhost:5000