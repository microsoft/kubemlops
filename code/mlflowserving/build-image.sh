# Get the model saved in mlflow.pyfunc format (mlflow.tensorflow.autolog() in train.py does that automatically)
export mlflowpod=$(kubectl get pod -l app.kubernetes.io/name=mlflow -n kubeflow -o jsonpath='{.items[*].metadata.name}')
export model_path=/mnt/azure/1/2072bc09fca64b348cb10f465d4eaebd/artifacts/model # for example
kubectl cp kubeflow/$mlflowpod:model_path ./model

# Check python version in model/conda.yaml

# Build scoring image
mlflow models build-docker -m model -n samplemodel

# Test image
python score.py 