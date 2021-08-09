# apewatch
Stream Reddit posts and comments containing stock tickers to Elasticsearch/Kibana for anomaly detection and alert to discord webhook.

## Find Investing Subreddits
`python3 no_brakes/subreddits.py`

## Stream submissions
`python3 no_brakes/submissions.py`

## Stream comments
`python3 no_brakes/comments.py`

## Generate client id and secret
https://www.reddit.com/prefs/apps

Put config.py in no_brakes
```
CLIENT_ID = ""
CLIENT_SECRET = ""
USERNAME = ""
PASSWORD = ""
```

## PROD
```
docker-compose -f docker-compose.yaml -f docker-compose-prod.yaml build
docker-compose -f docker-compose.yaml -f docker-compose-prod.yaml down
docker-compose -f docker-compose.yaml -f docker-compose-prod.yaml up -d
```

![MicrosoftTeams-image](https://user-images.githubusercontent.com/17228005/128655131-f70f17fd-5d0e-420e-8c51-3e0d5c0a987a.png)

