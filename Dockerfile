FROM python:3

ARG CAMERA
ARG CREDENTIALS_FILE
ENV CAMERA_NAME ${CAMERA}

COPY src .
COPY "${CREDENTIALS_FILE}" .

RUN pip install blinkpy

RUN mkdir images

CMD python run.py ${CAMERA_NAME}