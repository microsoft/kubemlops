import os
from flask import Flask, request
from kfp_teams_notifier import KfpTeamsNotifier, PIPELINE_OBJECT_TYPE, NODE_OBJECT_TYPE
import json


application = Flask(__name__)

@application.route("/notify", methods=['POST'])
def notify():
    payload = json.loads(request.get_data())# get_json()
    print(payload)
    
    teams_endpoint = os.getenv("TEAMS_ENDPOINT")
    kfp_endpoint = os.getenv("KFP_ENDPOINT")
    kfp_teams_notifier = KfpTeamsNotifier(teams_endpoint,kfp_endpoint)    

    node_name = payload["NodeName"]
    if node_name:
        object_type = NODE_OBJECT_TYPE
        object_name = node_name
    else:
        object_type = PIPELINE_OBJECT_TYPE
        object_name = payload["WorkflowName"]
        
    message = kfp_teams_notifier.notify(kfp_run_id=payload["KfpRunId"],
                              object_type=object_type,
                              object_name=object_name,
                              status=payload["EventType"],
                              message=payload["Message"]) 
    return message
        


if __name__ == "__main__":
    application.run(host='0.0.0.0')
