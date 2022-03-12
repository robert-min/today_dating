from kafka import KafkaConsumer
import json
import pymysql

brokers = ["localhost:9091", "localhost:9092", "localhost:9093"]
consumer = KafkaConsumer("place_db", bootstrap_servers=brokers)

for message in consumer:
    db = pymysql.connect(host="localhost", port=3306, user="root", password="aksen5466!", db="todayDating",
                         charset="utf8")
    try:
        msg = json.loads(message.value.decode())

        cursor = db.cursor()
        sql = """
        INSERT IGNORE INTO place (placeId, name, address, latitude, longitude, tel) VALUES ({0}, '{1}', '{2}', {3}, {4}, '{5}');
        """.format(
            int(msg["placeId"]),
            msg["name"],
            msg["address"],
            float(msg["latitude"]),
            float(msg["longitude"]),
            msg["tel"]
        )
        print(sql)
        cursor.execute(sql)
        db.commit()
    except:
        print("Error")

    finally:
        db.close()