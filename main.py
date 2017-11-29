#!/usr/bin/python3

import boto3
from picamera import PiCamera
from PIL import Image
from time import sleep
import datetime
import uuid
import io
import subprocess


def detect_faces(byte_image):

    response = rekognition.detect_faces(
        Image={
            'Bytes': byte_image
        }
    )

    faces_detected = response['FaceDetails']

    return faces_detected


def identify_face(image, byte_image):
    response = rekognition.detect_faces(
        Image={'Bytes': byte_image}
    )

    all_faces = response['FaceDetails']

    box = []

    # Get image diameters
    image_width = image.size[0]
    image_height = image.size[1]

    # Crop face from image
    for face in all_faces:
        box = face['BoundingBox']
        x1 = int(box['Left'] * image_width) * 0.9
        y1 = int(box['Top'] * image_height) * 0.9
        x2 = int(box['Left'] * image_width + box['Width'] * image_width) * 1.10
        y2 = int(box['Top'] * image_height + box['Height'] * image_height) * 1.10
        image_crop = image.crop((x1, y1, x2, y2))

        stream = io.BytesIO()
        image_crop.save(stream, format="JPEG")
        image_crop_binary = stream.getvalue()

    # with open('cropped-search.jpg', 'wb') as fb:
    # 	fb.write(image_crop_binary)

    # Submit individually cropped image to Amazon Rekognition
    response = rekognition.search_faces_by_image(
        CollectionId='family_collection',
        Image={'Bytes': image_crop_binary}
    )

    if len(response['FaceMatches']) > 0:
        # Return results
        print('Coordinates ', box)
        for match in response['FaceMatches']:

            face = dynamodb.get_item(
                TableName='family_collection',
                Key={'RekognitionId': {'S': match['Face']['FaceId']}}
            )

            if 'Item' in face:
                person = face['Item']['FirstName']['S']
                return person
            else:
                person = 'no match found'

            print(match['Face']['FaceId'], match['Face']['Confidence'], person)


def call_person(person):

    response = polly.synthesize_speech(OutputFormat='mp3', Text='Hello ' + person, VoiceId='Joanna')
    audio_bytes = response['AudioStream'].read()

    with open('./callmyname.mp3', 'wb') as fw:
        fw.write(audio_bytes)

    subprocess.call(['mpg321', './callmyname.mp3'])


def put_image(bucket, byte_image):

    s3.put_object(
        Body=byte_image,
        Bucket=bucket,
        Key='rekognition/archive' + str(uuid.uuid4()) + datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S') + '.jpeg'
    )


rekognition = boto3.client('rekognition', region_name='eu-west-1')
s3 = boto3.client('s3')
dynamodb = boto3.client('dynamodb', region_name='eu-west-1')
polly = boto3.client('polly', region_name='eu-west-1')

my_bucket = 'tlelet.com'
local_image = '/home/jiaming/Pictures/image_capture.jpeg'

# while True:
with PiCamera() as camera:

    camera.start_preview()

    # Camera warm-up time
    sleep(2)

    camera.resolution = (1280, 720)
    camera.capture(local_image, 'jpeg')

    image = Image.open(local_image)
    stream = io.BytesIO()
    image.save(stream, format="JPEG")
    image_binary = stream.getvalue()

    if len(detect_faces(image_binary)) == 0:
        print('No faces detected!')
    else:
        person = identify_face(image, image_binary)
        call_person(person)
        put_image(my_bucket, image_binary)


# compare_face() call should be put in a try...catch clause, in case files trying to read is not there
# use search_faces_by_image()? (or this function?) given an face image (me.jpg), find if any matching face in the target.
# call the person's name if face matches.

# store captured image locally first, compare and make decision. upload images that is different than the previous
# one for archive purpose.

# workflow: take picture -> store locally and compare -> send to s3 if different than previous one
# -> take picture without awaiting the completion of picture upload
# store file to s3 should be async, i.e. the program should start taking picture
# again, without awaiting the completion of the picture upload to s3.


# since a single image could contain multiple faces, we need to index them in a collection.
# then compare with pre-existing images..

# when put object to s3, put the person's full name in the metadata attribute.
# that can be used in the ddb table to correlate FaceId with the full name.


# if image is different than previous one, call cropImage module


