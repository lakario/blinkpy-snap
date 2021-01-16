FROM python:3

ARG CAMERA
ARG CREDENTIALS_FILE
ENV CAMERA_NAME ${CAMERA}

WORKDIR /appcode

COPY src .
COPY requirements.txt .
COPY "${CREDENTIALS_FILE}" .

RUN pip install -r requirements.txt

RUN mkdir images

CMD python run.py ${CAMERA_NAME}