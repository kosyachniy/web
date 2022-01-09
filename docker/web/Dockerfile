# Pull base image
FROM node:16.10 as web

# Set work directory
WORKDIR .

# Install dependencies
COPY ./package.json .
RUN npm install

# Copy project
COPY . .

# Settings
RUN rm -f src/sets.json
RUN echo '{ \n\
    "server": "'$PROTOCOL'://'$EXTERNAL_HOST'/api/", \n\
    "client": "'$PROTOCOL'://'$EXTERNAL_HOST'/", \n\
    "sockets": "'$PROTOCOL'://'$EXTERNAL_HOST'/", \n\
    "locale": "'$LOCALE'", \n\
    "timezone": '$TIMEZONE', \n\
    "name": "'$NAME'", \n\
    "mail": "'$EMAIL'", \n\
    "phone": "'$PHONE'", \n\
    "social": '$SOCIAL', \n\
    "amazon": { \n\
        "id": "'$AMAZON_ACCESS_ID'", \n\
        "key": "'$AMAZON_ACCESS_KEY'", \n\
        "bucket": "'$AMAZON_BUCKET_NAME'", \n\
        "dir": "'$AMAZON_DIR_NAME'", \n\
        "region": "'$AMAZON_REGION'" \n\
    }, \n\
    "maps": { \n\
        "center": { \n\
            "lat": '$GOOGLE_MAP_LAT', \n\
            "lng": '$GOOGLE_MAP_LNG' \n\
        }, \n\
        "zoom": '$GOOGLE_MAP_ZOOM', \n\
        "key": "'$GOOGLE_MAP_KEY'" \n\
    }, \n\
    "subscription": { \n\
        "day": '$SUBSCRIPTION_DAY', \n\
        "week": '$SUBSCRIPTION_WEEK', \n\
        "month": '$SUBSCRIPTION_MONTH', \n\
        "season": '$SUBSCRIPTION_SEASON', \n\
        "ay": '$SUBSCRIPTION_ACADEMIC_YEAR', \n\
        "year": '$SUBSCRIPTION_YEAR' \n\
    }, \n\
    "discount": '$DISCOUNT' \n\
} \n\
' >> src/sets.json

# Run
CMD npm start
