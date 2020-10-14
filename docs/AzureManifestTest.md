# Azure Manifest Tests
In order to make sure the Azure manifest on Kubeflow.org is functioning and user could install Kubeflow to AKS cluster. We design Azure Manifest tests to enable continously monitoring Azure Manifest.

## Parameters
Eight Parameters are defined in the Github action. It contains the information for the resource group to be created, the cluster size, and most importantly the url for Kubeflow and manifest. In order to make sure the latest version of Kubeflow and Manifest are being validated, check instruction here: https://www.kubeflow.org/docs/azure/deploy/install-kubeflow/, and make sure the manifest version and Kubeflow version are the one to be validated. The shell script code/tests/steps.sh would take those parameters and download the resource and install Kubeflow. 

## Availability Tests
The tests are two-fold. Firstly, we want to make sure that all pods are healthy, and, therefore, we have /code/tests/availability_tests.py. This test will make sure all the pods for Kubeflow will be up running within a pre-configured amount of time, currently it is 10 minutes. If any of the pods failed to be ready within this time frame, then the test will fail.

## Pipeline Tests
The /code/tests/manifest_tests will actually create a simple pipeline and execute the pipeline on the newly-claimed AKS cluster to validate that basic functionalities are available.

## Debug
Under normal circumstances, when the tests pass, all the resouces created for the tests will be deleted and the core will be released. However, if there are some errors caught during the tests, developers could go into the resource (Kubeflow dashboard) to inspect the run. To access the static IP, one needs to go to the ```Apply Resources``` stage of the Manifest_Test action and the static ip would be seen in the last command.