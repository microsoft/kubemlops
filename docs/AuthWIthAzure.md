# Instruction of enabling Oath 2.0 JWT authentication for the Kubeflow API with Azure AD

## Configure K8s cluster
* Upgrade [Istio to >=1.5](https://istio.io/docs/setup/getting-started/#download).
* Apply [requestauthingress.yaml](../kubernetes/requestauthingress.yaml). Update the file with your tenant id. 
  
## API calls
API is available on Istio Ingress endpoint with the request header "Authorization: Bearer TOKEN"
 
### Command line 
* Get the token
    ```
    curl -X POST -H "Content-Type: application/x-www-form-urlencoded" -d 'client_id=<SERVICE_PRINCIPAL>&scope=https%3A%2F%2Fgraph.microsoft.com%2F.default&client_secret=<SERVICE_PRINCIPAL_SECRET>&grant_type=client_credentials' 'https://login.microsoftonline.com/<TENANT>/oauth2/v2.0/token'
    ```

* Invoke API
    ```
    export ISTIO_ENDPOINT=$(kubectl -n istio-system get service istio-ingressgateway -o jsonpath='{.status.loadBalancer.ingress[0].ip}')
    curl http://$ISTIO_ENDPOINT/pipeline/apis/v1beta1/pipelines -H "Authorization: Bearer <TOKEN>"
    ```

### Python SDK
Consider the following code snippet to initialize a client with an auth token:

```python
token = get_access_token(tenant, service_principal, sp_secret)
client = kfp.Client(host=kfp_host, existing_token=token)
```

Look at the [sample code here](../code/sample_api.py)
    
  
## Dashboard
Dashboard is available through the port forwarding without any additional authentication:
```
kubectl port-forward svc/istio-ingressgateway  -n istio-system 8080:80
```
     
Open http://localhost:8080 in your browser. 