from azure.eventhub.aio import EventHubProducerClient
from azure.eventhub import EventData
import sys

async def run():
    length = len(sys.argv)
    for i in range(1, length):
        print(sys.argv[i])

    #Create a producer client to send messages to the event hub.
    #Specify a connection string to your event hubs namespace and
    #the event hub name.

    #producer = EventHubProducerClient.from_connection_string(conn_str="EVENT HUBS NAMESPACE - CONNECTION STRING", eventhub_name="EVENT HUB NAME")
    #async with producer:
    #    #Create a batch.
    #    event_data_batch = await producer.create_batch()

    #    #Add events to the batch.
    #    length = len(sys.argv)
    #    for i in range(1, length):
    #        event_data_batch.add(EventData(sys.argv[i]))
    #        print(sys.argv[i])

    #    #Send the batch of events to the event hub.
    #    await producer.send_batch(event_data_batch)


