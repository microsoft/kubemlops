# CD/Seldon-

In the kaizentm/kubemlops repository when a model is deployed, which is performed every time a model is successfully registered, the CD pipeline is triggered, and all jobs are run, which deploy to the following environments:

- QA
- UAT
- PROD

## Access CD pipeline via GitHub

1. Clicking on your pull request commit in GitHub actions, you will get the CI/Training pipeline steps. ![GitHub Commit CI](./diagrams/actions-commit-ci.png)
2. Clicking on “Model Training” on the left side and then “View more details”, you get all the GitHub actions associated with your pull request. ![GitHub PR Summary](./diagrams/pr-summary.png)
3. Clicking on “CD” on the left side, you get the details on failed and finished steps.

## Test deployed model

- Test with an image of a burrito:

```bash
curl -H "Content-Type: application/json" -d '{"image":"https://www.exploreveg.org/files/2015/05/sofritas-burrito.jpeg"}' http://bed8bac0-3663-4cb2-bcc5-99aa75f13562.eastus.azurecontainer.io/score`
```

- Test with an image of a taco:

```bash
curl -H "Content-Type: application/json" -d '{"image":"https://www.inspiredtaste.net/wp-content/uploads/2018/03/Easy-Ground-Pork-Tacos-Recipe-3-1200.jpg"}' http://bed8bac0-3663-4cb2-bcc5-99aa75f13562.eastus.azurecontainer.io/score
```
