
import requests
import string


PIPELINE_OBJECT_TYPE = 'PIPELINE'
NODE_OBJECT_TYPE = 'NODE'

WORKFLOW_FAILED_STATUS = 'WorkflowFailed'
WORKFLOW_SUCCEEDED_STATUS = 'WorkflowSucceeded'
WORKFLOW_START_STATUS = 'WorkflowRunning'
NODE_FAILED_STATUS = 'WorkflowNodeFailed'
NODE_SUCCEEDED_STATUS = 'WorkflowNodeSucceeded'

WORKFLOW_ERROR_MESSAGE_CARD_NAME = 'pipeline_error_message_card.json'
WORKFLOW_START_MESSAGE_CARD_NAME = 'pipeline_start_message_card.json'
WORKFLOW_FINISH_MESSAGE_CARD_NAME = 'pipeline_finish_message_card.json'

NODE_ERROR_MESSAGE_CARD_NAME = 'node_error_message_card.json'
NODE_FINISH_MESSAGE_CARD_NAME = 'node_finish_message_card.json'

class KfpTeamsNotifier:

    def __init__(self, teams_endpoint, kfp_endpoint):
        self.teams_endpoint = teams_endpoint
        self.kfp_endpoint = kfp_endpoint

    def get_payload_template_name(self, object_type, status)->str:        
        if (object_type == PIPELINE_OBJECT_TYPE):
            if (status == WORKFLOW_FAILED_STATUS):
                return WORKFLOW_ERROR_MESSAGE_CARD_NAME
            elif (status == WORKFLOW_SUCCEEDED_STATUS):
                return WORKFLOW_FINISH_MESSAGE_CARD_NAME
            elif (status == WORKFLOW_START_STATUS):
                return WORKFLOW_START_MESSAGE_CARD_NAME
            else:
                return None
        elif (object_type == NODE_OBJECT_TYPE):
            if (status == NODE_FAILED_STATUS):
                return NODE_ERROR_MESSAGE_CARD_NAME
            elif (status == NODE_SUCCEEDED_STATUS):
                return NODE_FINISH_MESSAGE_CARD_NAME
        else:
            return None

    def get_kfp_run_uri(self, kfp_run_id)->str:
        return f'{self.kfp_endpoint}/#/runs/details/{kfp_run_id}'



    def notify(self, kfp_run_id, object_type, object_name, status, message)->str:        
        payload = ""
        payload_template_name = self.get_payload_template_name(object_type, status)
        if (payload_template_name):
            with open(payload_template_name, 'r') as f:
                payload_template = f.read()
            if (payload_template):
                payload = string.Template(payload_template).substitute(kfp_run_id=kfp_run_id, object_name=object_name, status=status,
                message=message, kfp_run_uri=self.get_kfp_run_uri(kfp_run_id))                
                response = requests.post(self.teams_endpoint, payload)
                print(response.content)
                assert response.status_code == 200
        return payload

