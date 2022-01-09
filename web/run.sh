#!/bin/bash

rm -f src/sets.json
echo '{
    "server": "'$PROTOCOL'://'$EXTERNAL_HOST'/api/",
    "client": "'$PROTOCOL'://'$EXTERNAL_HOST'/",
    "sockets": "'$PROTOCOL'://'$EXTERNAL_HOST'/",
    "locale": "'$LOCALE'",
    "timezone": '$TIMEZONE',
    "name": "'$NAME'",
    "mail": "'$EMAIL'",
    "phone": "'$PHONE'",
    "social": '$SOCIAL',
    "amazon": {
        "id": "'$AMAZON_ACCESS_ID'",
        "key": "'$AMAZON_ACCESS_KEY'",
        "bucket": "'$AMAZON_BUCKET_NAME'",
        "dir": "'$AMAZON_DIR_NAME'",
        "region": "'$AMAZON_REGION'"
    },
    "maps": {
        "center": {
            "lat": '$GOOGLE_MAP_LAT',
            "lng": '$GOOGLE_MAP_LNG'
        },
        "zoom": '$GOOGLE_MAP_ZOOM',
        "key": "'$GOOGLE_MAP_KEY'"
    },
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
' >> src/sets.json
