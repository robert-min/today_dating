from kafka import KafkaConsumer
import json

brokers = ["localhost:9091", "localhost:9092", "localhost:9093"]
consumer = KafkaConsumer("blog_db", bootstrap_servers=brokers)

for message in consumer:
    msg = json.loads(message.value.decode())
    print(msg)