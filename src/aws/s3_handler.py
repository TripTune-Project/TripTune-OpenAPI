import boto3

class S3Handler:
    def __init__(self, region_name, bucket_name, aws_access_key_id, aws_secret_access_key):
        try:
            self.s3 = boto3.client(
                service_name = "s3",
                region_name = region_name,
                aws_access_key_id = aws_access_key_id,
                aws_secret_access_key = aws_secret_access_key,
            )
            self.bucket_name = bucket_name
            self.region_name = region_name

            print("s3 bucket connected!")
        except Exception as e:
            print(e)
            
    def upload_file(self, image_byte_arr, object_path):
        try:
            self.s3.upload_fileobj(image_byte_arr, self.bucket_name, object_path)
            
            object_url = "https://" + self.bucket_name + ".s3." + self.region_name + ".amazonaws.com/" + object_path
            return object_url
        except Exception as e:
            print("업로드 실패 : ", e)
    