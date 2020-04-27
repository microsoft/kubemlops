import os
import requests

class GhActionsClient:

    def __init__(self, repo, pat):
        self.owner, self.repo = repo.split("/")
        self.personal_access_token = pat

        self.base_url = f'https://api.github.com/repos/{self.owner}/{self.repo}'
        self.headers = {'authorization': f'token {self.personal_access_token}',
                   'accept': 'application/vnd.github.everest-preview+json'}

    def send_dispatch_event(self, sha, pr_num, phase):
        url = self.base_url + "/dispatches"
        payload = {'sha': sha, 'pr_num': pr_num}
        data = {'event_type': phase, 'client_payload': payload}
        response = requests.post(url=url, headers=self.headers, json=data)
        assert response.status_code == 204
        print(response)

    def add_comment(self, pr_num, comment):
        url = self.base_url + "/issues/{pr_num}/comments".format(pr_num=pr_num)        
        data = {'body': comment}
        response = requests.post(url=url, headers=self.headers, json=data)
        assert response.status_code == 201
        print(response)
        
def get_gh_actions_client():
    return GhActionsClient(os.getenv("GITHUB_TOKEN"), os.getenv("GITHUB_REPOSITORY"))

if __name__ == "__main__":
    
    repo = "kaizentm/kubemlops"
    client = GhActionsClient(repo, pat)
    client.send_dispatch_event(sha="", pr_num="6", phase="Model is registered")
    # client.add_comment(pr_num="6", comment="Hello from Client")



