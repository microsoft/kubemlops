FROM python:3.7-slim

ENV APP_HOME /app
ENV WORKERS 1
ENV THREADS 8
ENV PREDICTIVE_UNIT_SERVICE_PORT 8080
WORKDIR $APP_HOME
COPY pipeline.py requirements.txt ./
ENV PYTHONUNBUFFERED=1

RUN pip install --no-cache-dir -r ./requirements.txt

CMD ["sh","-c","gunicorn --bind 0.0.0.0:$PREDICTIVE_UNIT_SERVICE_PORT --workers $WORKERS --threads $THREADS pipeline"]