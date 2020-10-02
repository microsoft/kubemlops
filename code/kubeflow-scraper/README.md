# Kubeflow Scraper

## Overview

This is a set of config files that implement a Kubeflow scraper that exports data in Prometheus exposition format. It leverages the query-exporter project to periodically query the Kubeflow MySQL database and provide a Prometheus endpoint.

We currently make the following queries and data available:

- Kubeflow Pipelines run data including experiment, run id, workload id, etc
- Metadata DB data that links Kubeflow Pipeline run workloads to pods and step descriptions (avoids JSON parsing)

With this data exposed, we have a way to link run data to pods and therefore Kubernetes stats. We also avoid numerous queries to the KubeFlow Pipelines API and Metadata DB gRPC API, and avoid the need to parse the workflow JSON.

Example Grafana dashboards will be added soon.

## Install instructions

1. Create 'monitoring' namespace
   1. `kubectl create namespace monitoring`
2. Deploy kube-prometheus-stack
   1. `helm install -n monitoring kube-prometheus-stack prometheus-community/kube-prometheus-stack`
3. If you are currently using seldon-core-analytics, redeploy using the kube-prometheus-stack exporters so they don't step on each other
   1. `helm install seldon-core-analytics seldonio/seldon-core-analytics --namespace seldon-system --set prometheus.nodeExporter.enabled=false --set prometheus.kubeStateMetrics.enabled=false`
4. Create a read only user for scraping from kfp's mysql. If you have a separate metadata db, you will need to do the same for that one.
   1. Open a connection to kubeflow's mysql `kubectl port-forward svc/mysql -n kubeflow 3306:3306`
   2. Create a user with SELECT privileges only e.g. 'kfpexporter' and note the password
5. Update query-pod.yml db connection secret with the db creds you created
6. Deploy the config.yaml as a configmap
   1. `kubectl create configmap -n kubeflow kfp-exporter-config --from-file config.yaml`
7. Deploy the service, app deployment, secret, and ServiceMonitor
   1. `kubectl apply -f query-pod.yml`
8. Connect to grafana
   1. `kubectl port-forward -n monitoring svc/kube-prometheus-stack-grafana 8080:80`
9. Import the json dashboards
