from interface_with_gcp.cloud_storage.get_file import generate_signed_url_for_object
from n_gram.vector_n_gram_for_cloud_functions import vector_n_grams_cloud_functions
import json

from flask import Flask, request

app = Flask(__name__)


@app.route("/ngram", methods=['POST'])
def run_ngram():
    request_args = json.loads(request.data)
    filename = request_args['filename']
    url_of_data = generate_signed_url_for_object('access-cloud-storage-buckets', 'temporary-ads-data-storage', filename)
    # return url_of_data
    vector_n_grams_cloud_functions(
        request_args['roas_target'],
        request_args['filter_on_roas'],
        url_of_data,
        request_args['email'],
        False
    )
    return 'OK'


if __name__ == '__main__':
    app.run()
