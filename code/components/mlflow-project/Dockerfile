FROM python:3.7-slim

# ARG host
# ARG token

# ENV DATABRICKS_HOST=host
# ENV DATABRICKS_TOKEN=token

RUN pip install mlflow>=1.0 && \
    pip install databricks-cli && \
    apt-get update && \
    apt-get install git-all -y


COPY . /scripts/

WORKDIR /scripts

#ENTRYPOINT ["./run.sh"]
CMD [ "python3", "./run.py" ]
