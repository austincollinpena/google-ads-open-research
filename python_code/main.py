from interface_with_gcp.cloud_storage.get_file import generate_signed_url_for_object, get_file
from n_gram.n_gram_for_cloud_functions import n_gram_for_cloud_functions
import json

from flask import Flask, request

app = Flask(__name__)


@app.route("/ngram", methods=['POST'])
def run_ngram():
    request_args = json.loads(request.data)
    filename = request_args['filename']
    print("looking for", filename)
    url_of_data = generate_signed_url_for_object('access-cloud-storage-buckets', 'temporary-ads-data-storage', filename)
    # return url_of_data
    n_gram_for_cloud_functions(
        request_args['roas_target'],
        url_of_data,
        request_args['name'],
        False
    )
    return 'OK'


if __name__ == '__main__':
    app.run()
