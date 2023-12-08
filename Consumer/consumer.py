import asyncio
from azure.eventhub.aio import EventHubConsumerClient
from azure.eventhub.extensions.checkpointstoreblobaio import BlobCheckpointStore

BLOB_STORAGE_CONNECTION_STRING = "DefaultEndpointsProtocol=https;AccountName=lab1container;AccountKey=aK1n08UwataZH53JXOdWW3tCFosCcPzKK5wQNOirmfHgm/CJ7lE7611AbNWfKdfW5dGKNAReidVw+AStfSmo2A==;EndpointSuffix=core.windows.net"
BLOB_CONTAINER_NAME = "blobcontainer"
EVENT_HUB_CONNECTION_STR = "Endpoint=sb://tpiuolabos.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=hC9+ynrnSKy/0kQbOLfR8j6LTSKse0W33+AEhDAheHc="
EVENT_HUB_NAME = "labos1"

async def on_event(partition_context, event):
    print("Received event from partition: {}".format(partition_context.partition_id))
    print(event.body_as_str())

    await partition_context.update_checkpoint(event)

async def main():
    checkpoint_store = BlobCheckpointStore.from_connection_string(BLOB_STORAGE_CONNECTION_STRING, BLOB_CONTAINER_NAME)
    client = EventHubConsumerClient.from_connection_string(EVENT_HUB_CONNECTION_STR, 
                                                            consumer_group="$Default", 
                                                            eventhub_name=EVENT_HUB_NAME, 
                                                            checkpoint_store=checkpoint_store)
    async with client:
        await client.receive(on_event=on_event, starting_position="-1")

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    while True:
        pass        