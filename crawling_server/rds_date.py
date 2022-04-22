import json
import boto3
import secret
from time import time, localtime, strftime


s3r = boto3.resource("s3", aws_access_key_id=secret.aws_access_id, aws_secret_access_key=secret.aws_access_secret)
bucket = s3r.Bucket("today-dating")


# 어제 날짜에 모인 Json 파일 업로드
tm = localtime(time() - 86400)
date = strftime("%Y-%m-%d", tm)

# folder download
path = date

for object in bucket.objects.filter(Prefix=path):
    key = object.key
    body = object.get()["Body"]
    source = json.load(body)
    print(source)
