# docker build -t us-central1-docker.pkg.dev/totemic-fact-361111/python-analytics/rest_api:latest .
# docker push us-central1-docker.pkg.dev/totemic-fact-361111/python-analytics/rest_api:latest

# docker run us-central1-docker.pkg.dev/totemic-fact-361111/python-analytics/rest_api:latest

# gcloud run deploy public-python-analytics --image=us-central1-docker.pkg.dev/totemic-fact-361111/python-analytics/rest_api:latest --platform="managed" --region="us-central1" --project="totemic-fact-361111"

FROM python:3.10-slim

ENV PYTHONUNBUFFERED True
ENV PORT 8080

ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./

RUN pip install Flask gunicorn
RUN pip install -r requirements.txt


CMD exec gunicorn --bind :$PORT --workers 1 --threads 1 --timeout 0 main:app