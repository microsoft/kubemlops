NAMESPACE=serving

kubectl port-forward svc/pipeline-pipeline-predictor 8000:8000 -n $NAMESPACE
curl -v -H "Content-Type: application/json" -d '{"data":"0"}' http://localhost:8000/api/v0.1/predictions

CLUSTER_IP=$(kubectl -n istio-system get service istio-ingressgateway -o jsonpath='{.status.loadBalancer.ingress[0].ip}')
curl -v -H "Content-Type: application/json" -d '{"data":"0"}' $CLUSTER_IP/seldon/$NAMESPACE/pipeline/api/v0.1/predictions

