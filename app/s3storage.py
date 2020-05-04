import boto3
import os

URL_FORMAT = "https://s3-{region}.amazonaws.com/{bucketName}/{imageName}"

class S3Storage():

    def __init__(self):

        self.region = os.getenv("AWS_REGION")
        self.s3_resource = boto3.resource(
            's3',
            aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY"),
            region_name = self.region
            )

    def uploadTo(self, bucketName, userId, imageName, data):
        self.bucketName = bucketName
        self.imageName = "{userId}_{imageName}".format(
            userId = userId,
            imageName = imageName
            )
        
        self.s3_resource.Bucket(bucketName).put_object(
            Key = self.imageName,
            Body = data
        )


    def getUrl(self):
        url = URL_FORMAT.format(
            region = self.region,
            bucketName = self.bucketName,
            imageName = self.imageName
        )

        return url