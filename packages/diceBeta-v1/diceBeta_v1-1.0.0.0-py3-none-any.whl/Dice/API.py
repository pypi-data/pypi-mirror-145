# -*- coding: utf-8 -*- 
#pip install google-cloud-storage
import os
from google.cloud import storage
import requests

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/kim-yeong-geun/Documents/gcp_key.json" 


def upload_to_bucket(blob_name, path_to_file, bucket_name):
    """ Upload data to a bucket(아까 만들었던 저장소)"""

 
    storage_client = storage.Client.from_service_account_json(
        "/Users/kim-yeong-geun/Downloads/elite-striker-343511-7d5c4076a0ba.json" )
    #print(buckets = list(storage_client.list_buckets())

    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(blob_name)
    blob.upload_from_filename(path_to_file)
    
    #접근권한 public 으로 설정
    #blob.make_public()
    
    #파일 url 만들어주기
    url = blob.public_url
    #returns a public url
    return url

def run_api(path='', mode='inference'):
    token_url = "http://3.39.109.198:8000/list/" + mode + "/"
    config = {'url': path}
    result = requests.post(token_url, data = config)
    print(result.text)

    return result.text

def run(data, mode='inference'):
    #"https://storage.googleapis.com/nnc-gifticon/KakaoTalk_20220404_123923047_01.jpg"
    blob_name = "test_folder/test." + data.split(".")[-1]
    bucket_name = "nnc-gifticon"
    url = upload_to_bucket(blob_name, data, bucket_name)
    run_api(path=url, mode=mode)

def inferAPI(data):
    run(data, mode='inference')

def trainAPI(data):
    run(data, mode='train')

if __name__ == '__main__':
    data = "/Users/kim-yeong-geun/Downloads/13776.jpg"
    inferAPI(data)