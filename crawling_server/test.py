from pyspark.sql import SparkSession

MAX_MEMORY = "5g"
spark = SparkSession.builder.appName("today_dating")\
    .config("spark.executor.memory", MAX_MEMORY)\
    .config("spark.driver.memory", MAX_MEMORY)\
    .getOrCreate()


df = spark.read.parquet("./parquet/test.parquet")
df.printSchema()