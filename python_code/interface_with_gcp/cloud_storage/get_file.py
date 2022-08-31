import os

from service_account_management.return_credentials import return_credentials
from google.oauth2 import service_account
from google.cloud import storage
from datetime import datetime, timedelta
import logging


def get_file(service_account_name: str, bucket_name: str, file_name: str):
    json_credentials = return_credentials(service_account_name)
    credentials = service_account.Credentials.from_service_account_info(json_credentials)
    storage_client = storage.Client(credentials=credentials)
    bucket = storage_client.bucket(bucket_name)
    return bucket.blob(file_name)


def generate_signed_url_for_object(service_account_name: str, bucket_name: str, file_name: str):
    logging.info("trying to generate for presigned url2")
    print("trying to generate for presigned url")
    json_credentials = return_credentials(service_account_name)
    credentials = service_account.Credentials.from_service_account_info(json_credentials)
    logging.info("have credentials for presigned url")
    storage_client = storage.Client(credentials=credentials)
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.get_blob(file_name)
    return blob.generate_signed_url(expiration=(datetime.utcnow() + timedelta(minutes=2)))


if __name__ == "__main__":
    os.chdir("../../")
    print(os.getcwd())
    url = generate_signed_url_for_object("access-cloud-storage-buckets", "temporary-ads-data-storage", "search_terms.csv")
    print(url)
