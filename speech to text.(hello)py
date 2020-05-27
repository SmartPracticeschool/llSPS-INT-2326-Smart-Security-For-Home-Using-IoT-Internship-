import json
from os.path import join, dirname
from ibm_watson import SpeechToTextV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
authenticator = IAMAuthenticator('F81s0KCKqAmAvZMErULa2x5pFKRVxKaQ0whfHiEsqOKZ')
speech_to_text = SpeechToTextV1(
    authenticator=authenticator
)
speech_to_text.set_service_url('https://api.au-syd.speech-to-text.watson.cloud.ibm.com/instances/26b487b3-9f78-466e-aefc-f493c3583c7d')
with open(join(dirname(__file__), './.', 'hello.mp3'),
               'rb') as audio_file:
    results = speech_to_text.recognize(
        audio=audio_file,
        content_type='audio/mp3',
    ).get_result()
a=results['results'][0]['alternatives'][0]['transcript']
print(a)


if a[0:5]=='hello':
    print("recognzed")
else:
    print("not recognized")
