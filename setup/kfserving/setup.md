[Install Istio-1.5.4](https://istio.io/docs/setup/getting-started/#download)

[Install Knative 0.14.0](https://knative.dev/docs/install/any-kubernetes-cluster/)

[Install KFServing](https://github.com/kubeflow/kfserving)

```TAG=v0.3.0
CONFIG_URI=https://raw.githubusercontent.com/kubeflow/kfserving/master/install/$TAG/kfserving.yaml
kubectl apply -f ${CONFIG_URI}
```

