import os, io, glob
from urllib import response
from google.cloud import vision
from google.cloud import storage
from google.cloud.vision_v1 import types
import pandas as pd
from google.protobuf import json_format
import re

from oauth2client.service_account import ServiceAccountCredentials

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'ServiceAccountToken.json'

credentials = storage.Client.from_service_account_json('ServiceAccountToken.json')

client = storage.Client()

bucket = client.get_bucket('bucket_ottoman')
blob = bucket.blob('Tercüman-ı Hakikat_upload.pdf')
blob.upload_from_filename('Tercüman-ı Hakikat_upload.pdf')

def read_file_blob(bucket_name, destination_blob_name):
    """Read a file from the bucket."""
 
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.download_to_filename('f1.json')

    # read as string
    read_output = blob.download_as_string()
 
    print(
        "File {} read successfully  from Bucket  {}.".format(
            destination_blob_name, bucket_name
        )
    )
    #print(read_output)
    with open('f.json', 'w+') as f:
        f.write(str(read_output))


read_file_blob('bucket_ottoman_out', 'Envar_Zeka_1.pdf_ocr.pdfoutput-1-to-10.json')
