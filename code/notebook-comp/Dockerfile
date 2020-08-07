FROM python:3.7-slim

# pip install
COPY requirements.txt /scripts/requirements.txt
RUN pip install --upgrade pip &&\
    pip install -r /scripts/requirements.txt

# only for local testing
COPY src/program.py /scripts/program.py
COPY notebook/experiment.ipynb /scripts/experiment.ipynb
COPY notebook/experiment.ipynb /scripts/output.ipynb

# will be overwritten by kf pipeline
ENTRYPOINT [ "python", "/scripts/program.py" ]
