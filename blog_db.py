from kafka import KafkaConsumer
import pymysql
import json

brokers = ["localhost:9091", "localhost:9092", "localhost:9093"]
consumer = KafkaConsumer("blog_db", bootstrap_servers=brokers)

db = pymysql.connect(host="localhost", port=3306, user="root", password="aksen5466!", db="todayDating", charset="utf8")

for message in consumer:
    msg = json.loads(message.value.decode())
    print(msg["keyword"])
    try:
        cursor = db.cursor()
        sql = "INSERT IGNORE INTO blog (keyword, title, link, placeId) VALUES ('{0}', '{1}', '{2}', {3});".format(
            msg["keyword"],
            msg["title"],
            msg["link"],
            int(msg["placeId"])
        )
        print(sql)
        cursor.execute(sql)

        db.commit()
    finally:
        db.close()


