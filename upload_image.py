"""
Example:

python3 upload_image.py --file /PATH/TO/image.JPG --first-name FIRST_NAME --full-name FULL_NAME --bucket S3_BUCKET_NAME
--prefix PATH/TO/IMAGE.jpg"

Note.

No forward slash in front of the PATH in PATH/TO/IMAGE.jpg
"""


import boto3
import argparse

s3 = boto3.client('s3', region_name='eu-west-1')


def index_faces():

    parser = argparse.ArgumentParser()
    parser.add_argument("--file", help="specify a image to upload.")
    parser.add_argument("--first-name", help="Please specify the first name of the person in the image.")
    parser.add_argument("--full-name", help="Please specify the full name of the person in the image.")
    parser.add_argument("--bucket-name", help="Please specify the bucket name to store the image.")
    parser.add_argument("--prefix", help="Please specify the path (exclude bucket name) to the image.")

    args = parser.parse_args()

    with open(args.file, 'rb') as fr:
        image_bytes = fr.read()
        s3.put_object(Body=image_bytes,
                      Bucket=args.bucket_name,
                      Key=args.prefix,
                      Metadata={'fullname': args.full_name,
                                'firstname': args.first_name
                                }
                      )


if __name__ == '__main__':
    index_faces()
