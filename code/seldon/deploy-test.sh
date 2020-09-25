NAMESPACE=seldon

kubectl apply -f deployment.yaml -n $NAMESPACE

kubectl port-forward svc/mexicanfood-mexicanfood-predictor 8000:8000 -n $NAMESPACE
curl -v -H "Content-Type: application/json" -d '{"image":"https://www.inspiredtaste.net/wp-content/uploads/2018/03/Easy-Ground-Pork-Tacos-Recipe-3-1200.jpg"}' http://localhost:8000/api/v0.1/predictions

CLUSTER_IP=$(kubectl -n istio-system get service istio-ingressgateway -o jsonpath='{.status.loadBalancer.ingress[0].ip}')
curl -v -H "Content-Type: application/json" -d '{"image":"https://www.inspiredtaste.net/wp-content/uploads/2018/03/Easy-Ground-Pork-Tacos-Recipe-3-1200.jpg"}' $CLUSTER_IP/seldon/$NAMESPACE/mexicanfood/api/v0.1/predictions

# To test canary deployment
curl -v -H "Content-Type: application/json" -d '{"image":"https://www.inspiredtaste.net/wp-content/uploads/2018/03/Easy-Ground-Pork-Tacos-Recipe-3-1200.jpg"}' $CLUSTER_IP/seldon/$NAMESPACE/mexicanfood-canary/api/v0.1/predictions

