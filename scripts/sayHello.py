import boto3

polly = boto3.client('polly', region_name='eu-west-1')

response = polly.synthesizespeech(OutputFormat='mp3', Text='Hello Joanna', VoiceId='Joanna')

mp3_bytes = response['AudioStream'].read()

with open('./Joanna.mp3', 'wb') as mp3:
    mp3.write(mp3_bytes)