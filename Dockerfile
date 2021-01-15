FROM python:3

ARG CREDENTIALS_FILE=credentials.json

COPY src .
COPY ${CREDENTIALS_FILE} .

RUN pip install blinkpy

RUN mkdir images

CMD ["python", "run.py"]