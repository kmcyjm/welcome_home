
import boto3
from picamera import PiCamera
from PIL import Image
from time import sleep
import datetime
import uuid
import io
import subprocess

class WelcomeHome(object):

    def detect_faces(byte_image):

        response = rekognition.detect_faces(
            Image={
                'Bytes': byte_image
            }
        )

        faces = response['FaceDetails']

        return faces


    def identify_faces(image, faces):

        person = []

        box = []

        # Get image diameters
        image_width = image.size[0]
        image_height = image.size[1]

        # Crop face from image
        for face in faces:
            box = face['BoundingBox']
            x1 = int(box['Left'] * image_width) * 0.9
            y1 = int(box['Top'] * image_height) * 0.9
            x2 = int(box['Left'] * image_width + box['Width'] * image_width) * 1.10
            y2 = int(box['Top'] * image_height + box['Height'] * image_height) * 1.10
            image_crop = image.crop((x1, y1, x2, y2))
            #
            stream = io.BytesIO()
            image_crop.save(stream, format="JPEG")
            image_crop_binary = stream.getvalue()

            # Submit individually cropped image to Amazon Rekognition
            response = rekognition.search_faces_by_image(
                CollectionId='family_collection',
                Image={'Bytes': image_crop_binary}
            )

            if len(response['FaceMatches']) > 0:

                print('Coordinates ', box)
                for match in response['FaceMatches']:

                    face = dynamodb.get_item(
                        TableName='family_collection',
                        Key={'RekognitionId': {'S': match['Face']['FaceId']}}
                    )

                    if 'Item' in face:
                        person_name = face['Item']['FirstName']['S']

                        if person_name == 'Juan':
                            person.append(person_name)
                            return person
                        else:
                            person.append(person_name)
                            print(match['Face']['FaceId'], match['Face']['Confidence'], person)
                    else:
                        print("You've added the family photo in S3. However, you might forgotten to add" +
                              person + "to the family list in the DynamoDB table.")
            else:
                print("This person isn't in your family collection. You may consider to add a new collection.")

        return person


    def call_person(person):

        names = ''

        for i in person:
            names = names + ' ' + i

        if names.strip() == 'Juan':
            input_text = "hola juan, has tenido un buen día hoy?"
        else:
            input_text = "Welcome home " + names + ", did you have a good day today?"

        response = polly.synthesize_speech(OutputFormat='mp3', Text=input_text, VoiceId='Joanna')
        audio_bytes = response['AudioStream'].read()

        with open('./callmyname.mp3', 'wb') as fw:
            fw.write(audio_bytes)

        subprocess.call(['mpg321', './callmyname.mp3'])


    def put_image(bucket, byte_image):

        s3.put_object(
            Body=byte_image,
            Bucket=bucket,
            Key='rekognition/archive/' + str(uuid.uuid4()) + '_' + datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S') + '.jpeg'
        )


    rekognition = boto3.client('rekognition', region_name='eu-west-1')
    s3 = boto3.client('s3')
    dynamodb = boto3.client('dynamodb', region_name='eu-west-1')
    polly = boto3.client('polly', region_name='eu-west-1')

    my_bucket = 'tlelet.com'
    local_image = '/tmp/image.jpeg'

while True:
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

        all_faces = detect_faces(image_binary)

        if len(all_faces) == 0:
            print('No faces detected!')
        else:
            person = identify_faces(image, all_faces)
            call_person(person)
            put_image(my_bucket, image_binary)



