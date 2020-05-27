from ibm_watson import TextToSpeechV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from playsound import playsound

authenticator = IAMAuthenticator('jXgCcQ2zY5-RNGwl_qmtBcbMfOQVyfjw3QK_06SdiYg0')
text_to_speech = TextToSpeechV1(
    authenticator=authenticator
)

text_to_speech.set_service_url('https://api.au-syd.text-to-speech.watson.cloud.ibm.com/instances/a76acb39-4c36-4d12-8c85-6c5bf75224ca')

with open('help.mp3', 'wb') as audio_file:
    audio_file.write(
        text_to_speech.synthesize(
            'Help',
            voice='en-US_AllisonVoice',
            accept='audio/mp3'        
        ).get_result().content)
playsound("help.mp3")
