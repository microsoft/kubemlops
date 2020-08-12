FROM python:3.7-slim

# ARG host
# ARG token

# ENV DATABRICKS_HOST=host
# ENV DATABRICKS_TOKEN=token

# Build prereqs for psutil
RUN apt-get update && \
    apt-get install -y python3-dev gcc

# Private pip repo
ARG PIP_EXTRA_INDEX_URL

RUN pip install mlflow>=1.0 && \
    pip install databricks-cli && \
    pip install kubemlops-logging==0.1.dev1 && \
    apt-get update && \
    apt-get install git-all -y


COPY . /scripts/

WORKDIR /scripts

#ENTRYPOINT ["./run.sh"]
CMD [ "python3", "./run.py" ]
