# Welcome home!

This project uses the camera on a Rasbperry Pi to taking pictures, and recognize persons' face in the picture. In case any faces matching the ones on record, it will play an audio to speak the person's name. 


## More info wanted?

In case you want to know more about what happens behind the scenes, please read on. Otherwise, you can skip to the [Prerequisites](#prerequisites) Prerequisites section.

The main program runs on an Rasbperry Pi with a camera connected. It uses the camera to take image continously, and upload them to AWS Rekognition to detect faces. Each face will be assigned with an unique UUID, which is used by Rekognition to identify the person. This unique id is also used as the partition key in DynamoDB, where the metadata of the person is stored. In case the detected faces match any faces stored in DynamoDB, the persons' name will be sent to AWS Polly to be synthesized into a mp3 file. The mp3 file is then played on Rasbperry Pi.


##<a name="prerequisites"></a>Prerequisites

1. An AWS account.
2. Rasbperry Pi with a camera. (preferably with 1080P resolution)

## Installation

**Note.**

>The following process (except for uploading the script to Rasbperry Pi and run it there) can be automated by using a CloudFormation template, which will be attached here later on.

1. Create a S3 bucket to store face images.

	Using AWS SDK or CLI to upload the image which should only contain the face of one person. 
	
	Please send the metadata (e.g. first name) of the person along with the image to S3. These attributes will be stored in the DynamoDB table, and will be used to synthesize the person' name.  
	

2. Create a Lambda function to index the faces in the image, and store the person's metadata in a DynamoDB table.


	```python
	lambda function code goes here.
	```


3. Use the Event Notification function on the S3 bucket to trigger the Lambda function created in step 2, to index the faces in the image.


4. The face recognition program keeps running on the Raspberry Pi. From there, it keeps taking pictures, and calling AWS Rekognition service to detect faces in the image. If any faces detected in the image, they will be cropped out individually, and sent to match the faces stored in the DynamoDB table. 

	In case any matching faces found in DynamoDB table, the first name of the individual person to which each face belongs to, will be concatenated and sent to AWS Polly for speech synthesizing.
	
	The default text synthesized is,
	
	"Hello [NAMEs], did you have a good day today?" 
	
	The synthesized audio will be stored locally on Rasbperry Pi, and played out via the speaker.
	