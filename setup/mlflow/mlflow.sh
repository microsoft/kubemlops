# https://hub.kubeapps.com/charts/larribas/mlflow
helm repo add larribas https://larribas.me/helm-charts
helm install mlflow larribas/mlflow --set image.repository="dtzar/mlflow",image.tag="latest",extraArgs.expose-prometheus="yes"

# Access the UI
k port-forward svc/mlflow 5000:5000
http://localhost:5000