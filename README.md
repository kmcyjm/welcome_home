# Welcome home!
-

This whole project needs to run on Rasbperry Pi. It uses the camera to take image at certain interval, upload them to AWS Rekognition to see any faces are detected. If any faces is detected, it then proceed to match the faces (i.e. the metadata of the faces) stored in DynamoDB. In case of a match, the program  then pulls the person's name in the DynamoDB, and send it to AWS Polly to be synthesized into a mp3 file. The mp3 file is then played on Rasbperry Pi to speak the persons' name.

## Usage

To be updated.