FROM python:3.10-slim-buster

WORKDIR /appcode

COPY requirements.txt .
RUN pip install -r requirements.txt
COPY src .

CMD python run.py -q