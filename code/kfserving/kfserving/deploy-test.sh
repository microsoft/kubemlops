MODEL_NAME=mexicanfood
INGRESS_GATEWAY=kfserving-ingressgateway
CLUSTER_IP=$(kubectl -n istio-system get service $INGRESS_GATEWAY -o jsonpath='{.status.loadBalancer.ingress[0].ip}')
SERVICE_HOSTNAME=$(kubectl get inferenceservice ${MODEL_NAME} -o jsonpath='{.status.url}' -n kubeflow | cut -d "/" -f 3)

curl -v -H "Host: ${SERVICE_HOSTNAME}" -d '{"image":"https://www.inspiredtaste.net/wp-content/uploads/2018/03/Easy-Ground-Pork-Tacos-Recipe-3-1200.jpg"}' http://$CLUSTER_IP/v1/models/${MODEL_NAME}:predict