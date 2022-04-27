# -*- coding: utf-8 -*-

from time import time, gmtime
from naver_api import NaverApi
from kafka import KafkaConsumer

# kafka producer
brokers = ["localhost:9091", "localhost:9092", "localhost:9093"]
consumer = KafkaConsumer(bootstrap_servers=brokers)

for message in consumer:
    try:
        keyword = message
        tm = gmtime(time())
        date_data = NaverApi(keyword)
        date_data.save_json(tm)
        date_data.save_list(tm)
    except:
        pass