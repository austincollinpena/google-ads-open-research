import os
import json


# return_credentials is a helper function to
def return_credentials(file_path: str):

    with open(f'./service_accounts/{file_path}.json', 'r') as f:
        return json.load(f)


if __name__ == "__main__":
    credentials = return_credentials("access-cloud-storage-buckets")
