# Initialize variables:
# AZ_SUBSCRIPTION_ID=
# AZ_TENANT_ID=
# AZ_CLIENT_ID=
# AZ_CLIENT_SECRET=
# KUBEFLOW_NAMESPACE=kubeflow

kubectl create secret generic azcreds --from-literal=AZ_SUBSCRIPTION_ID=$AZ_SUBSCRIPTION_ID \
                                      --from-literal=AZ_TENANT_ID=$AZ_TENANT_ID \
                                      --from-literal=AZ_CLIENT_ID=$AZ_CLIENT_ID \
                                      --from-literal=AZ_CLIENT_SECRET=$AZ_CLIENT_SECRET \
                                      -n $KUBEFLOW_NAMESPACE
