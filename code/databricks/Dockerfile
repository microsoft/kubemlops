FROM python:3.7-slim

# pip install
RUN pip install databricks-cli && \
    apt-get update && apt-get install jq -y

COPY notebook.py /scripts/notebook.py
COPY run_config.json /scripts/run_config.json
COPY run_notebook.sh /scripts/run_notebook.sh

# will be overwritten by kf pipeline
ENTRYPOINT [ "sh", "-c", "/scripts/run_notebook.sh" ]
