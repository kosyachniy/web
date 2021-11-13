# Pull base image
FROM python:3.9.7

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
ARG PROTOCOL HOST MODE SIDE_OPTIMIZED LOCALE TIMEZONE \
    MONGO_DB MONGO_LOGIN MONGO_PASSWORD SMSC_LOGIN SMSC_PASSWORD \
    GOOGLE_ID GOOGLE_SECRET TG_TOKEN BUG_CHAT VK_ID VK_SECRET \
    YOOKASSA_ID YOOKASSA_KEY \
    SUBSCRIPTION_DAY SUBSCRIPTION_WEEK SUBSCRIPTION_MONTH SUBSCRIPTION_SEASON \
    SUBSCRIPTION_ACADEMIC_YEAR SUBSCRIPTION_YEAR DISCOUNT
RUN rm -f sets.json
RUN echo '{ \n\
    "mongo": { \n\
        "host": "db", \n\
        "db": "'$MONGO_DB'", \n\
        "login": "'$MONGO_LOGIN'", \n\
        "password": "'$MONGO_PASSWORD'" \n\
    }, \n\
    "yookassa": { \n\
        "id": '$YOOKASSA_ID', \n\
        "key": "'$YOOKASSA_KEY'" \n\
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
    "client": "'$PROTOCOL'://'$HOST'/", \n\
    "mode": "'$MODE'", \n\
    "side_optimized": '$SIDE_OPTIMIZED', \n\
    "locale": "'$LOCALE'", \n\
    "timezone": '$TIMEZONE', \n\
    "bug_chat": '$BUG_CHAT', \n\
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
' >> sets.json
