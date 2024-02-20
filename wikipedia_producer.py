import json
import time
import random #only for sample data

from kafka import KafkaProducer #refers to kafka-python

ORDER_KAFKA_TOPIC = "wikipedia_events"
EVENT_LIMIT = 500

# create a dictionary for known namespaces https://en.wikipedia.org/wiki/Wikipedia:Namespace#Programming
namespace_dict = {-2: 'Media',
                  -1: 'Special',
                  0: 'main namespace',
                  1: 'Talk',
                  2: 'User', 3: 'User Talk',
                  4: 'Wikipedia', 5: 'Wikipedia Talk',
                  6: 'File', 7: 'File Talk',
                  8: 'MediaWiki', 9: 'MediaWiki Talk',
                  10: 'Template', 11: 'Template Talk',
                  12: 'Help', 13: 'Help Talk',
                  14: 'Category', 15: 'Category Talk',
                  100: 'Portal', 101: 'Portal Talk',
                  108: 'Book', 109: 'Book Talk',
                  118: 'Draft', 119: 'Draft Talk',
                  446: 'Education Program', 447: 'Education Program Talk',
                  710: 'TimedText', 711: 'TimedText Talk',
                  828: 'Module', 829: 'Module Talk',
                  2300: 'Gadget', 2301: 'Gadget Talk',
                  2302: 'Gadget definition', 2303: 'Gadget definition Talk'}


# https://kafka-python.readthedocs.io/en/master/apidoc/KafkaProducer.html
producer = KafkaProducer(bootstrap_servers="localhost:29092")

print("generate sample Wikipedia eventdata, according do recentchange json sturcture")
print("Will generate one unique event every 0-1 seconds, beginning in 5 seconds..")
time.sleep(5)

# construct sample data
for i in range(1, EVENT_LIMIT):
    data = {
        "id": i,
        "domain": f"{random.choice(['commons', 'de', 'en', 'uk'])}.wikimedia.org",
        "namespace": random.choice(list(namespace_dict.values())),  # resolved namespace name
        "title": f"sample_title{i}",
        "timestamp": int(time.time()),
        "user_name": f"sample_user{i}",
        "user_type": random.choice(['bot', 'human']),
        "old_length": i,
        "new_length": i+1,
    }

    producer.send(ORDER_KAFKA_TOPIC, json.dumps(data).encode("utf-8"))
    print(f"Done Sending..{i}")
    time.sleep(random.random())  # random sleep time between 0 and 1 in float
