import boto3
import subprocess

polly = boto3.client('polly', region_name='eu-west-1')

response = polly.synthesize_speech(OutputFormat='mp3', Text='Hello Joanna', VoiceId='Joanna')

mp3_bytes = response['AudioStream'].read()

with open('./Joanna.mp3', 'wb') as mp3:
    mp3.write(mp3_bytes)

subprocess.call(['mpg321', '/home/jiaming/welcome_home/Joanna.mp3'])
