import json
import datetime

from kafka import KafkaConsumer #refers to kafka-python
from kafka import KafkaProducer


EVENT_KAFKA_TOPIC = "wikipedia_events"
EVENT_AGG_KAFKA_TOPIC = "wikipedia_events_agg"


consumer = KafkaConsumer(
    EVENT_KAFKA_TOPIC,
    bootstrap_servers="localhost:29092",
)
producer = KafkaProducer(bootstrap_servers="localhost:29092")


print("consumer start listening")
while True:
    for event in consumer:
        consumed_event = json.loads(event.value.decode())
        print(consumed_event)

        # extract minutes string from unixtime
        timestamp = consumed_event["timestamp"]
        timestamp_in_minutes = datetime.datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M')

        # create bool for german domains
        domain = consumed_event["domain"]
        if domain.split(".")[0] == "de":
            is_de_domain = True
        else:
            is_de_domain = False

        data = {
            "timestamp": timestamp,
            "timestamp_in_minutes": timestamp_in_minutes,
            "is_de_domain": is_de_domain,
        }

        producer.send(EVENT_AGG_KAFKA_TOPIC, json.dumps(data).encode("utf-8"))
