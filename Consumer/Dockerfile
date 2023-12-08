FROM python:3.9

WORKDIR /app

COPY consumer.py /app

RUN pip install asyncio  azure-eventhub azure-eventhub-checkpointstoreblob-aio aiohttp

CMD [ "python", "./consumer.py" ]