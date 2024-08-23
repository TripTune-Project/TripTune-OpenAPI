import boto3

class S3Handler:
    def __init__(self, region_name, aws_access_key_id, aws_secret_access_key):
        try:
            self.s3 = boto3.client(
                service_name = "s3",
                region_name = region_name,
                aws_access_key_id = aws_access_key_id,
                aws_secret_access_key = aws_secret_access_key,
            )
            print("s3 bucket connected!")
        except Exception as e:
            print(e)
            
        

    