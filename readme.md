# Streaming and aggregating sample wikipedia events using Kafka-Python #

## set-up environment ##

### prerequisites: this setup assumes running a local Docker Container and executing python scripts on a windows machine ###

- installed and running docker instance like [docker-desktop](https://www.docker.com/products/docker-desktop/)
- installed latest [python3](https://www.python.org/downloads/windows/) release 

Using ```docker-compose up -d ```, you'll create a docker container that is running a minimal config instance of zookeeper and kafka running on localhost. 
The requirements.txt contains all needed python packages, or you can manually install [kafka-python](https://pypi.org/project/kafka-python/) yourself.


## Script Schema Overview ##

![img](pictures/kafka%20schema.png)

#### wikipedia_producer.py ####
creates sample data according to [Wikipedia recent change](https://stream.wikimedia.org/v2/stream/recentchange) API for demonstration purposes and writes them to wikipedia_events kafka topic every 0-1 second.
In the script, you can edit the EVENT_LIMIT variable to change the sample generation output.

#### wikipedia_consumer.py ####
Consumes the raw wikipedia_events output, transform it into JSON and extents the wikipedia_events topic with a datetime(YMDHM) and a geofilter for german wikipedia servers, that is used in the analytics script.

#### wikipedia_analytics.py ####
Consumes the edited wikipedia_events_agg stream and calculates the avg changes in the global and german wiki servers and writes them with the according timestamp to events_per_minute.json file.


## Notes ##

The project ist to demonstrate a simple kafka pipeline with microservices for later extension with mature services and scalability.
The Wikipedia_Producer can hook up the WikipediaRecentchange SSE stream for real data; the Wikipedia_Consumer can perform heavier cleanup and transformation with ie. K-SQL
and the Wikipedia_Analytics can write the output to databases like mongoDB, or elasticsearch for data analysis.



