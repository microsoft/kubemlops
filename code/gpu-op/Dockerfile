FROM pytorch/pytorch:latest

# pip install
COPY requirements.txt /scripts/requirements.txt
RUN pip install -r /scripts/requirements.txt

COPY src/program.py /scripts/program.py

ENTRYPOINT [ "python", "/scripts/program.py"]

