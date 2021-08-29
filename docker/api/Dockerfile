# Pull base image
FROM python:3.9.1

# Set work directory
WORKDIR .

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
# NOTE: Using Russian text may lead to errors 0, 137
# Output print to the Docker console
ENV PYTHONUNBUFFERED 1

# Install dependencies
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# Copy project
COPY . .

# Settings
ARG PROTOCOL HOST PORT MODE SIDE_OPTIMIZED LOCALES LOCALE TIMEZONE \
    MONGO_DB MONGO_LOGIN MONGO_PASSWORD SMSC_LOGIN SMSC_PASSWORD \
    GOOGLE_ID GOOGLE_SECRET TG_TOKEN BUG_CHAT VK_ID VK_SECRET
RUN rm -f sets.json
RUN echo '{ \n\
    "mongo": { \n\
        "host": "db", \n\
        "db": "'$MONGO_DB'", \n\
        "login": "'$MONGO_LOGIN'", \n\
        "password": "'$MONGO_PASSWORD'" \n\
    }, \n\
    "google": { \n\
        "client_id": "'$GOOGLE_ID'", \n\
        "client_secret": "'$GOOGLE_SECRET'" \n\
    }, \n\
    "tg": { \n\
        "token": "'$TG_TOKEN'" \n\
    }, \n\
    "vk": { \n\
        "client_id": '$VK_ID', \n\
        "client_secret": "'$VK_SECRET'" \n\
    }, \n\
    "smsc": { \n\
        "login": "'$SMSC_LOGIN'", \n\
        "password": "'$SMSC_PASSWORD'" \n\
    }, \n\
    "client": "'$PROTOCOL'://'$HOST':'$PORT'/", \n\
    "mode": "'$MODE'", \n\
    "side_optimized": '$SIDE_OPTIMIZED', \n\
    "locales": '$LOCALES', \n\
    "locale": "'$LOCALE'", \n\
    "timezone": '$TIMEZONE', \n\
    "bug_chat": '$BUG_CHAT' \n\
} \n\
' >> sets.json

# Run
CMD bash run.sh
