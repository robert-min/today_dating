import boto3
import secret
import os
from pyspark.sql import SparkSession

MAX_MEMORY = "5g"
spark = SparkSession.builder.appName("today_dating") \
    .config("spark.executor.memory", MAX_MEMORY) \
    .config("spark.driver.memory", MAX_MEMORY) \
    .getOrCreate()

s3r = boto3.resource("s3", aws_access_key_id=secret.aws_access_id, aws_secret_access_key=secret.aws_access_secret)
bucket = s3r.Bucket("today-dating")

# folder download
path = "date-blog/test.parquet"
for obj in bucket.objects.filter(Prefix=path):
    print(obj)