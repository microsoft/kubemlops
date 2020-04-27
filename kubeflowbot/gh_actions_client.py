import requests

class Gh_actions_client:

    def __init__(self, repo, pat):
        self.owner, self.repo = repo.split("/")
        self.personal_access_token = pat

        self.base_url = f'https://api.github.com/repos/{self.owner}/{self.repo}'
        self.headers = {'authorization': f'token {self.personal_access_token}',
                   'accept': 'application/vnd.github.everest-preview+json'}

    def send_dispatch_event(self, sha, pr_num, phase):
        payload = {'sha': sha, 'pr_num': pr_num, 'phase': phase}
        url = self.base_url + "/dispatches"
        data = {'event_type': f'{payload}'}
        response = requests.post(url=url, headers=self.headers, json=data)
        assert response.status_code == 204
        print(response)

if __name__ == "__main__":
    
    repo = "kaizentm/kubemlops"
    client = Gh_actions_client(repo, pat)
    client.send_dispatch_event(sha="", pr_num="", phase="training")
