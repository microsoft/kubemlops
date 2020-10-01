FROM python:3.7-slim

ENV APP_HOME /app
ENV WORKERS 1
ENV THREADS 8
ENV PORT 8000

WORKDIR $APP_HOME
COPY src/* ./

RUN pip install -r ./requirements.txt                                  


CMD ["sh","-c","gunicorn --bind 0.0.0.0:$PORT --workers $WORKERS --threads $THREADS api"]