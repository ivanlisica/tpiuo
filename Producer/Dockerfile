FROM python:3.9

WORKDIR /app

COPY producer.py /app

RUN pip install requests  azure-eventhub

CMD [ "python", "./producer.py" ]