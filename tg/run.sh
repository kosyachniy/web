#!/bin/bash

rm -f sets.json
echo '{
    "server": "'$PROTOCOL'://'$EXTERNAL_HOST'/api/",
    "client": "'$PROTOCOL'://'$EXTERNAL_HOST'/",
    "tg": {
        "name": "'$TG_BOT'",
        "server": "'$PROTOCOL'://'$EXTERNAL_HOST'/tg/",
        "token": "'$TG_TOKEN'"
    },
    "amazon": {
        "key": "'$AMAZON_ACCESS_ID'",
        "secret": "'$AMAZON_ACCESS_KEY'",
        "bucket": "'$AMAZON_BUCKET_NAME'",
        "directory": "'$AMAZON_DIR_NAME'",
        "region": "'$AMAZON_REGION'"
    },
    "mode": "'$MODE'",
    "bug_chat": '$BUG_CHAT'
}
' >> sets.json

python app.py
