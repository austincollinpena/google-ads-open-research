 functions-framework --target=run_ngram
 
gcloud functions deploy ngram-optimizer --gen2 --runtime=python310 --source=. --entry-point=run_ngram --trigger-http --allow-unauthenticated --project=totemic-fact-361111 --region=us-central1 --verbose debug