# Pull base image
FROM node:17.3 as web

# Set work directory
WORKDIR .

# Install dependencies
COPY ./package.json .
RUN npm install

# Copy project
COPY . .

# Settings
ARG PROTOCOL HOST LOCALE TIMEZONE NAME MAIL PHONE SOCIAL \
    GOOGLE_MAP_KEY GOOGLE_MAP_LAT GOOGLE_MAP_LNG GOOGLE_MAP_ZOOM \
    SUBSCRIPTION_DAY SUBSCRIPTION_WEEK SUBSCRIPTION_MONTH SUBSCRIPTION_SEASON \
    SUBSCRIPTION_ACADEMIC_YEAR SUBSCRIPTION_YEAR DISCOUNT
RUN rm -f src/sets.json
RUN echo '{ \n\
    "server": "'$PROTOCOL'://'$HOST'/api/", \n\
    "sockets": "'$PROTOCOL'://'$HOST'/", \n\
    "locale": "'$LOCALE'", \n\
    "timezone": '$TIMEZONE', \n\
    "name": "'$NAME'", \n\
    "mail": "'$MAIL'", \n\
    "phone": "'$PHONE'", \n\
    "social": '$SOCIAL', \n\
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
