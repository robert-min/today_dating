import boto3
import secret
import os
from pyspark.sql import SparkSession
from pyspark.sql import SQLContext

# MAX_MEMORY = "5g"
# spark = SparkSession.builder.appName("today_dating") \
#     .config("spark.executor.memory", MAX_MEMORY) \
#     .config("spark.driver.memory", MAX_MEMORY) \
#     .getOrCreate()

# s3r = boto3.resource("s3", aws_access_key_id=secret.aws_access_id, aws_secret_access_key=secret.aws_access_secret)
# bucket = s3r.Bucket("today-dating")

# folder download
# path = "date-blog/test.parquet"
# df = spark.read.parquet(path)
# df.show()

# for obj in bucket.objects.filter(Prefix=path):
#     print(obj)

import pyspark
from pyspark.sql import SQLContext

sc = pyspark.SparkContext.getOrCreate()
sqlContext = SQLContext(sc)
df = sqlContext.read.parquet("./parquet/test.parquet")
# df.select("blog").show()

for i in df.select("blog"):
    print(i)

sc.stop()