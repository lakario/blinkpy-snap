FROM python:3

COPY src .

RUN pip install blinkpy

CMD ["python", "run.py"]