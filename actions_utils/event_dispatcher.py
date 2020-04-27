import os
import json
from gh_actions_client import get_gh_actions_client


class EventDispatcher:

    REGISTER_MODEL_EVENT = "Model is registered"
    MODEL_REGISTRATION_COMMENT = "Model {model_name} has been registered \
                                  at the [model registry](microsoft.com) \
                                  with the following metrics {metrics}"

    def __init__(self, event_payload_file):
        with open(event_payload_file, 'r') as f:
            raw_payload = json.load(f)
            print("Payload")
            print(raw_payload)
            self.event_payload = eval(raw_payload['action'])
            print("Payload")
            print(self.event_payload)
        
        self.event_type = self.event_payload['event_type']
        if ('client_payload' in self.event_payload):
            self.event_client_payload = self.event_payload['client_payload']
        else:
            self.event_client_payload = None

    def add_comment(self, comment):        
        if ('pr_num' in self.event_client_payload):
            pr_num = self.event_client_payload['pr_num']            
            get_gh_actions_client().add_comment(pr_num, comment)


    # TODO: Fetch params from MLFlow
    def get_model_params(self):
        return {'model_name': 'Mexican Food', 
                'metrics': 'Spice level:10.0'}

    def handle_model_regsitered(self):        
        model_params = self.get_model_params() 
        comment = self.MODEL_REGISTRATION_COMMENT.format(model_name=model_params['model_name'],
                                                  metrics=model_params['metrics'])
        self.add_comment(comment)

    def dispatch(self):
        if (self.REGISTER_MODEL_EVENT==self.event_type):
            self.handle_model_regsitered()


if __name__ == "__main__":
    event_dispatcher = EventDispatcher(os.getenv('GITHUB_EVENT_PATH'))
    event_dispatcher.dispatch() 