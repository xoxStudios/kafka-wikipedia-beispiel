import json
from collections import defaultdict

from kafka import KafkaConsumer


EVENT_AGG_KAFKA_TOPIC = "wikipedia_events_agg"


consumer = KafkaConsumer(
    EVENT_AGG_KAFKA_TOPIC,
    bootstrap_servers="localhost:29092",
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)


# init dictionaries to count events per minute
events_per_minute = defaultdict(int)
german_events_per_minute = defaultdict(int)

print("analytics start listening")

for event in consumer:

    # global counter
    timestamp_in_minutes = event.value['timestamp_in_minutes']
    events_per_minute[timestamp_in_minutes] += 1

    # german counter (transformed in wikipedia_consumer.py)
    is_de_domain = event.value['is_de_domain']
    if is_de_domain:
        german_events_per_minute[timestamp_in_minutes] += 1

    print("Aktuelle Edits pro Minute:")
    for minute, event_count in events_per_minute.items():
        print(f"Global:{minute}: {event_count}")
    for minute, event_count in german_events_per_minute.items():
        print(f"German:{minute}: {event_count}")

    events_per_minute_values = list(events_per_minute.values())
    german_events_per_minute_values = list(german_events_per_minute.values())

    # save both global/german events per minute in json file for sample simplicity
    with open('events_per_minute.json', 'w') as file:
        json.dump({
            "Event-Minute": list(events_per_minute.keys()),
            "Global": events_per_minute_values,
            "German": german_events_per_minute_values
        }, file)
