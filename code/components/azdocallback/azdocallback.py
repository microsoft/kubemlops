import base64
import json
import requests
import time
import argparse
import kfp
import adal
import os


def info(msg, char="#", width=75):
    print("")
    print(char * width)
    print(char + "   %0*s" % ((-1 * width) + 5, msg) + char)
    print(char * width)


def send_complete_event(callbackinfo, pat, status):  # noqa: E501
    callback_vars = json.loads(callbackinfo.replace("'", '"'))  # noqa: E501
    url = r"{planUri}/{projectId}/_apis/distributedtask/hubs/{hubName}/plans/{planId}/events?api-version=2.0-preview.1".format(                           # noqa: E501
        planUri=callback_vars["PlanUri"], projectId=callback_vars["ProjectId"], hubName=callback_vars["HubName"], planId=callback_vars["PlanId"])          # noqa: E501
    data = {'name': 'TaskCompleted',
            'taskId': callback_vars["TaskInstanceId"], 'jobId': callback_vars["JobId"], 'result': status}   # noqa: E501
    header = {'Authorization': 'Basic ' + pat}
    response = requests.post(url, json=data, headers=header)
    print(response)
    # Raise an exception on failure code, otherwise no-op
    response.raise_for_status()


def get_component_status(kfp_host_url, kfp_run_id, token=None):
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


def get_pat(pat_env, pat_path_env):
    if pat_env:
        # Read PAT from env var
        pat = os.environ[pat_env]
    elif pat_path_env:
        # Read PAT from file
        with open(os.environ[pat_path_env], 'r') as f:
            pat = f.readline()
        f.close
    else:
        raise Exception('Please provide a PAT via pat_env or pat_path_env')
    pat = ":" + pat
    return str(base64.b64encode(pat.encode("utf-8")), "utf-8")


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
    parser.add_argument('-ppe', '--pat_path_env',
                        help='Name of environment variable containing the path to the Azure DevOps PAT')  # noqa: E501
    parser.add_argument('-pe', '--pat_env',
                        help='Name of environment variable containing the Azure DevOps PAT')  # noqa: E501
    args = parser.parse_args()

    pat = get_pat(args.pat_env, args.pat_path_env)

    status = get_component_status(args.kfp_host_url, args.run_id, get_access_token(    # noqa: E501
        args.tenant_id, args.service_principal_id, args.service_principal_password))  # noqa: E501
    send_complete_event(args.azdocallback, pat, status)
