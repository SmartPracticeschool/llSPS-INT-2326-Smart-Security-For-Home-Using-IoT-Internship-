import json
from os.path import join, dirname
from ibm_watson import SpeechToTextV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import cv2
import numpy as np
import datetime
import ibm_boto3
from ibm_botocore.client import Config, ClientError
from playsound import playsound
from cloudant.client import Cloudant
from cloudant.error import CloudantException
from cloudant.result import Result, ResultByKey

#It will read the first frame/image of the video
video=cv2.VideoCapture(0)

face_classifier=cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

authenticator = IAMAuthenticator('F81s0KCKqAmAvZMErULa2x5pFKRVxKaQ0whfHiEsqOKZ')
speech_to_text = SpeechToTextV1(
    authenticator=authenticator
)
speech_to_text.set_service_url('https://api.au-syd.speech-to-text.watson.cloud.ibm.com/instances/26b487b3-9f78-466e-aefc-f493c3583c7d')

COS_ENDPOINT = "https://s3.jp-tok.cloud-object-storage.appdomain.cloud" # Current list avaiable at https://control.cloud-object-storage.cloud.ibm.com/v2/endpoints
COS_API_KEY_ID = "0ic2LN_Lle86XvjBAft-BrTyCaFWwzxQGfnKH6Ryds7o" # eg "W00YiRnLW4a3fTjMB-odB-2ySfTrFBIQQWanc--P3byk"
COS_AUTH_ENDPOINT = "https://iam.cloud.ibm.com/identity/token"
COS_RESOURCE_CRN = "crn:v1:bluemix:public:cloud-object-storage:global:a/fbf65509580645fba6b9c6048de4e823:2c5780c1-1e7f-469b-8760-7b33c30c52cf::" # eg "crn:v1:bluemix:public:cloud-object-storage:global:a/3bf0d9003abfb5d29761c3e97696b71c:d6f04d83-6c4f-4a62-a165-696756d63903::"

# Create resource
cos = ibm_boto3.resource("s3",
    ibm_api_key_id=COS_API_KEY_ID,
    ibm_service_instance_id=COS_RESOURCE_CRN,
    ibm_auth_endpoint=COS_AUTH_ENDPOINT,
    config=Config(signature_version="oauth"),
    endpoint_url=COS_ENDPOINT
)


client = Cloudant("e110f3bc-b2e8-483b-9c09-7ebd72c72c1b-bluemix", "962ef67bd0897965b5ce8d4964fee0cf992c757adb5a35a6c185163dda592dbf", url="https://e110f3bc-b2e8-483b-9c09-7ebd72c72c1b-bluemix:962ef67bd0897965b5ce8d4964fee0cf992c757adb5a35a6c185163dda592dbf@e110f3bc-b2e8-483b-9c09-7ebd72c72c1b-bluemix.cloudantnosqldb.appdomain.cloud")
client.connect()
#Provide your database name

database_name = "sample"
my_database = client.create_database(database_name)
if my_database.exists():
   print(f"'{database_name}' successfully created.")



def audiofile(a):
    with open(join(dirname(__file__), './.', a),
                   'rb') as audio_file:
        results = speech_to_text.recognize(
            audio=audio_file,
            content_type='audio/mp3',
        ).get_result()
    b=results['results'][0]['alternatives'][0]['transcript']
    print(b)
    if b[0:4]=="help":
        cam()
    elif b[0:5]=="hello":
        print("system activated")
    else:
        print("give the correct input")


def multi_part_upload(bucket_name, item_name, file_path):
    try:
        print("Starting file transfer for {0} to bucket: {1}\n".format(item_name, bucket_name))
        # set 5 MB chunks
        part_size = 1024 * 1024 * 5

        # set threadhold to 15 MB
        file_threshold = 1024 * 1024 * 15

        # set the transfer threshold and chunk size
        transfer_config = ibm_boto3.s3.transfer.TransferConfig(
            multipart_threshold=file_threshold,
            multipart_chunksize=part_size
        )

        # the upload_fileobj method will automatically execute a multi-part upload
        # in 5 MB chunks for all files over 15 MB
        with open(file_path, "rb") as file_data:
            cos.Object(bucket_name, item_name).upload_fileobj(
                Fileobj=file_data,
                Config=transfer_config
            )

        print("Transfer for {0} Complete!\n".format(item_name))
    except ClientError as be:
        print("CLIENT ERROR: {0}\n".format(be))
    except Exception as e:
        print("Unable to complete multi-part upload: {0}".format(e))

    

def cam():
    while True:
        #capture the first frame
        check,frame=video.read()
        gray=cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        #detect the faces from the video using detectMultiScale function
        faces=face_classifier.detectMultiScale(gray,1.3,5)
        
        print(faces)
        
        #drawing rectangle boundries for the detected face
        for(x,y,w,h) in faces:
            cv2.rectangle(frame, (x,y), (x+w,y+h), (127,0,255), 2)
            cv2.imshow('Face detection', frame)
            cv2.imwrite("face.jpg",frame)
            multi_part_upload("pujithkatragadda2", "pujith.jpg", r"face.jpg")
            json_document={"link":COS_ENDPOINT+"/"+"pujithkatragadda2"+"/pujith.jpg"}
            new_document = my_database.create_document(json_document)
            # Check that the document exists in the database.
            if new_document.exists():
               print(f"Document successfully created.")

        #waitKey(1)- for every 1 millisecond new frame will be captured
        Key=cv2.waitKey(1)
        if Key==ord('q'):
            #release the camera
            video.release()
            #destroy all windows
            cv2.destroyAllWindows()

a="help.mp3"
playsound(a)
audiofile(a)




