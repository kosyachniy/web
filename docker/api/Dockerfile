# Pull base image
FROM python:3.9.1

# Set work directory
WORKDIR .

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
# Using Russian text may lead to errors 0, 137
# Output print to the Docker console
ENV PYTHONUNBUFFERED 1

# Install dependencies
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# Copy project
COPY . .

# Settings
ARG PROTOCOL HOST PORT MODE SIDE_OPTIMIZED MONGO_LOGIN MONGO_PASSWORD \
    GOOGLE_ID GOOGLE_SECRET TG_TOKEN BUG_CHAT SMSC_LOGIN SMSC_PASSWORD VK_ID \
    VK_SECRET
RUN rm -f sets.json keys.json
RUN echo '{ \n\
    "mongo": { \n\
        "host": "db", \n\
        "db": "uple" \n\
    }, \n\
    "client": "'$PROTOCOL'://'$HOST':'$PORT'/", \n\
    "mode": "'$MODE'", \n\
    "side_optimized": '$SIDE_OPTIMIZED', \n\
    "bug_chat": '$BUG_CHAT' \n\
} \n\
' >> sets.json
RUN echo '{ \n\
    "mongo": { \n\
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
    "smsc": { \n\
        "login": "'$SMSC_LOGIN'", \n\
        "password": "'$SMSC_PASSWORD'" \n\
    }, \n\
    "vk": { \n\
        "client_id": '$VK_ID', \n\
        "client_secret": "'$VK_SECRET'" \n\
    } \n\
} \n\
' >> keys.json

# Run
CMD bash run.sh
