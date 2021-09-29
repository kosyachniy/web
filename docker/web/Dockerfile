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
ARG PROTOCOL HOST PORT LOCALES LOCALE TIMEZONE NAME MAIL PHONE SOCIAL \
    GOOGLE_MAP_KEY GOOGLE_MAP_LAT GOOGLE_MAP_LNG GOOGLE_MAP_ZOOM
RUN rm -f src/sets.json
RUN echo '{ \n\
    "server": "'$PROTOCOL'://'$HOST':'$PORT'/api/", \n\
    "sockets": "'$PROTOCOL'://'$HOST':'$PORT'/", \n\
    "locales": '$LOCALES', \n\
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
    } \n\
} \n\
' >> src/sets.json

# Run
CMD npm start
