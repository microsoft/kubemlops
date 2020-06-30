# CI/Pull Request

In the kaizentm/kubemlops repository, when a pull request is created, the CI pipeline is triggered, but only the code_quality_check job is run by default. If either the build_images or build_pipeline job is necessary, then the PR must contain the comment “/build-images” or ‘/build-pipeline’.

## Trigger CI/PR Pipeline

1. Make a non-breaking change to a file in the kaizentm/kubemlops repository.
2. Commit the change via Git
3. Create a pull request via Git

## Access your pull request via GitHub

After creating the pull request, you can find your pull request in Git Hub Actions

1. Clicking on `Actions` tab at the top and `CI` on the left side, you will find your pull request. ![GitHub CI Actions](./diagrams/actions-ci.png)
2. Clicking on your pull request, you will get more details on failed, finished, and skipped jobs. Clicking on the job will get you more details on failed, finished, and skipped steps.![GitHub CI Job Steps](./diagrams/actions-ci-pr.png)