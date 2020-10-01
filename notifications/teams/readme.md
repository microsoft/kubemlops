# A component to send notifications to the Teams channel

* [Configure a webhook to a Teams channel](https://outlook.office.com/webhook/a315bacc-7165-47a2-8d6a-41eea6eab577@72f988bf-86f1-41af-91ab-2d7cd011db47/IncomingWebhook/a01d08fe51dd40b1bbfa2734e9e369af/e7c72e9f-4c72-4fa5-a1d2-c88bbdd65b5e) and update kfpteamsnotifier.yml with the webhook uri.
* Apply kfpteamsnotifier.yml
```
kubectl apply -f kfpteamsnotifier.yml -n kubeflow
```
* Port forward the service 
```
kubectl port-forward svc/kfpteamsnotifier-svc 8000:8000 -n kubeflow
```
* Send a message 
 ```
 curl  -d '{"kfp_run_id":"1222-2534-534534-54543","object_type":"PIPELINE","object_name":"my_pipeline","status":"Failed","message":"It's my fault"}' http://127.0.0.1:8000/notify
 ```

 This component can be used by a KFP exit handler or (preferable) it can be subscribed on KFP events broadcasting by [KFP Events Handler](https://github.com/kaizentm/kfp-event-handler).