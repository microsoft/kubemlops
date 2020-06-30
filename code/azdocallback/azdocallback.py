import json
import requests
import time
import argparse
import kfp
import adal


def info(msg, char="#", width=75):
    print("")
    print(char * width)
    print(char + "   %0*s" % ((-1 * width) + 5, msg) + char)
    print(char * width)


def send_complete_event(callbackinfo, status):  # noqa: E501
    callback_vars = json.loads(callbackinfo.replace("'", '"'))  # noqa: E501
    url = r"{planUri}/{projectId}/_apis/distributedtask/hubs/{hubName}/plans/{planId}/events?api-version=2.0-preview.1".format(                           # noqa: E501
        planUri=callback_vars["PlanUri"], projectId=callback_vars["ProjectId"], hubName=callback_vars["HubName"], planId=callback_vars["PlanId"])          # noqa: E501
    data = {'name': 'TaskCompleted',
            'taskId': callback_vars["TaskInstanceId"], 'jobId': callback_vars["JobId"], 'result': status}   # noqa: E501
    header = {'Authorization': 'Bearer ' + callback_vars["AuthToken"]}
    response = requests.post(url, json=data, headers=header)
    print(response)


def get_compoenet_status(kfp_host_url, kfp_run_id, token=None):
    status = "Suceeded"
    client = kfp.Client(host=kfp_host_url,
                        existing_token=token)
    run_response = client.get_run(kfp_run_id)
    workflow_manifest = json.loads(
        run_response.pipeline_runtime.workflow_manifest)  # noqa: E501
    time.sleep(5)  # Current status from Argo to Kubeflow takes time
    for (k, v) in workflow_manifest['status']['nodes'].items():
        if(v['type'] == "Pod"):
            if(v['phase'] == "Failed"):
                status = "failed"
                info("Failed Component: " + v['displayName'])

    return status


def get_access_token(tenant, clientId, client_secret):
    authorityHostUrl = "https://login.microsoftonline.com"
    GRAPH_RESOURCE = '00000002-0000-0000-c000-000000000000'

    authority_url = authorityHostUrl + '/' + tenant

    context = adal.AuthenticationContext(authority_url)
    token = context.acquire_token_with_client_credentials(GRAPH_RESOURCE, clientId, client_secret)  # noqa: E501
    return token['accessToken']


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Azure DevOps Callback')
    parser.add_argument('-hst', '--kfp_host_url',
                        help='Kubeflow Host Url')
    parser.add_argument('-azcb', '--azdocallback',
                        help='Azure DevOps call back Info')
    parser.add_argument('-id', '--run_id',
                        help='Kubeflow Pipeline Run Id')
    parser.add_argument('-t', '--tenant_id', help='tenant_id')
    parser.add_argument('-s', '--service_principal_id',
                        help='service_principal_id')
    parser.add_argument('-p', '--service_principal_password',
                        help='service_principal_password')
    args = parser.parse_args()

    status = get_compoenet_status(args.kfp_host_url, args.run_id, get_access_token(    # noqa: E501
        args.tenant_id, args.service_principal_id, args.service_principal_password))  # noqa: E501
    send_complete_event(args.azdocallback, status)
