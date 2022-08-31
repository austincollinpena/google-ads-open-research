import os

from service_account_management.return_credentials import return_credentials
from google.oauth2 import service_account
from google.cloud import storage


def upload_file(filename, file, service_account_name, bucket_name):
    json_credentials = return_credentials(service_account_name)
    credentials = service_account.Credentials.from_service_account_info(json_credentials)
    storage_client = storage.Client(credentials=credentials)
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(filename)
    blob.upload_from_file(file)


if __name__ == "__main__":
    os.chdir("../../")
    print(os.getcwd())
    with open("./readme.md", 'r') as f:
        url = upload_file("readme.md", f, "access-cloud-storage-buckets", "temporary-ads-data-storage")
