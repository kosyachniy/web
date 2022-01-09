#!/bin/bash

rm -f sets.json
echo '{
    "name": "'$PROJECT_NAME'",
    "mongo": {
        "host": "db",
        "db": "'$PROJECT_NAME'",
        "login": "'$MONGO_LOGIN'",
        "password": "'$MONGO_PASSWORD'"
    },
    "yookassa": {
        "id": '$YOOKASSA_ID',
        "key": "'$YOOKASSA_KEY'"
    },
    "google": {
        "client_id": "'$GOOGLE_ID'",
        "client_secret": "'$GOOGLE_SECRET'"
    },
    "amazon": {
        "key": "'$AMAZON_ACCESS_ID'",
        "secret": "'$AMAZON_ACCESS_KEY'",
        "bucket": "'$AMAZON_BUCKET_NAME'",
        "directory": "'$AMAZON_DIR_NAME'",
        "region": "'$AMAZON_REGION'"
    },
    "tg": {
        "token": "'$TG_TOKEN'",
        "bot": "'$TG_BOT'"
    },
    "vk": {
        "client_id": '$VK_ID',
        "client_secret": "'$VK_SECRET'"
    },
    "smsc": {
        "login": "'$SMSC_LOGIN'",
        "password": "'$SMSC_PASSWORD'"
    },
    "client": "'$PROTOCOL'://'$EXTERNAL_HOST'/",
    "mode": "'$MODE'",
    "side_optimized": '$SIDE_OPTIMIZED',
    "locale": "'$LOCALE'",
    "timezone": '$TIMEZONE',
    "bug_chat": '$BUG_CHAT',
    "subscription": {
        "day": '$SUBSCRIPTION_DAY',
        "week": '$SUBSCRIPTION_WEEK',
        "month": '$SUBSCRIPTION_MONTH',
        "season": '$SUBSCRIPTION_SEASON',
        "ay": '$SUBSCRIPTION_ACADEMIC_YEAR',
        "year": '$SUBSCRIPTION_YEAR'
    },
    "discount": '$DISCOUNT'
}
' >> sets.json
