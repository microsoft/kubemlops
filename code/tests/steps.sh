# Create AKS resources
mkdir kubeflow
cd kubeflow
# Download and install Kubeflow
curl -LO $1
tar -xvf $2
export BASE_DIR=$(pwd)
echo base dir is ${BASE_DIR}
export PATH=$PATH:$(pwd)
export KF_NAME=kf-test
export KF_DIR=${BASE_DIR}/${KF_NAME}
mkdir -p ${KF_DIR}
cd ${KF_DIR}
echo kf dir is ${KF_DIR}
kfctl -h
# Install istio
curl -L https://istio.io/downloadIstio | ISTIO_VERSION=1.6.8 TARGET_ARCH=x86_64 sh -
cd istio-1.6.8
export PATH=$PWD/bin:$PATH
istioctl install --set profile=demo
kubectl label namespace default istio-injection=enabled
cd ${KF_DIR}
echo currently at $(pwd)
echo ${PATH}
kfctl apply -V -f $3
echo Getting External Ip
echo $(kubectl -n istio-system get service istio-ingressgateway -o jsonpath='{.status.loadBalancer.ingress[0].ip}')