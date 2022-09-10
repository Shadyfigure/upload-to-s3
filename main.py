import os
import sys
import boto3
import shutil
from os import listdir
from os.path import isfile, join
import botocore.exceptions

s3 = boto3.resource('s3')

for bucket in s3.buckets.all():
    print(bucket.name)


print(sys.argv)

path = sys.argv[1]
dest = sys.argv[2]
bucket = sys.argv[3]
counter = 0

for f in listdir(path):
    file = join(path, f)
    if isfile(file):
        try:
            s3.Object(bucket, f).load()
            print('Exists: ' + f)
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == '404':
                print('Uploading: ' + f)
                with open(file, 'rb') as data:
                    s3.Bucket(bucket).put_object(Key=f, Body=data)
                    counter += 1
            else:
                print(e)

        shutil.move(file, dest + "\\" + f)

print("Finished uploading with count: " + str(counter));
