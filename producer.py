import requests
import requests.auth
import asyncio
from azure.eventhub import EventData
from azure.eventhub.aio import EventHubProducerClient
import json

CLIENT_ID = "yvoUh3kEBCCwrq7bsIfj8w"
SECRET_KEY = "IK-lzjqXxZ2M-wBssnpztBOO05LwoQ"

EVENT_HUB_CONNECTION_STR = "Endpoint=sb://tpiuolabos.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=hC9+ynrnSKy/0kQbOLfR8j6LTSKse0W33+AEhDAheHc="
EVENT_HUB_NAME = "labos1"

async def run():
    auth = requests.auth.HTTPBasicAuth(CLIENT_ID, SECRET_KEY)
    data = {
    'grant_type': 'password',
    'username': 'ivanlisica1609',
    'password': 'AzLe9t7e'
    }
    header = {'User-Agent': 'MyAPI/0.0.1'}
    res = requests.post('https://www.reddit.com/api/v1/access_token',auth=auth, data=data, headers=header)
    TOKEN = res.json()['access_token']
    header = {**header, **{'Authorization': f"bearer {TOKEN}"}}

    res = requests.get('https://oauth.reddit.com/r/dataengineering/top', headers=header, params={'t': 'all', 'limit': 10})
    data = res.json()

    client = EventHubProducerClient.from_connection_string(conn_str=EVENT_HUB_CONNECTION_STR, eventhub_name=EVENT_HUB_NAME)
    
    async with client:
        event_data_batch = await client.create_batch()
        for post in data['data']['children']:
            event_data = EventData(json.dumps(post))
            event_data_batch.add(event_data)

        await client.send_batch(event_data_batch)    

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
    while True:
        pass
