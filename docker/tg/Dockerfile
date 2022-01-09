# Pull base image
FROM python:3.9.9

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
RUN rm -f sets.json
RUN echo '{ \n\
    "server": "'$PROTOCOL'://'$EXTERNAL_HOST'/api/", \n\
    "client": "'$PROTOCOL'://'$EXTERNAL_HOST'/", \n\
    "tg": { \n\
        "name": "'$TG_BOT'", \n\
        "server": "'$PROTOCOL'://'$EXTERNAL_HOST'/tg/", \n\
        "token": "'$TG_TOKEN'" \n\
    }, \n\
    "amazon": { \n\
        "key": "'$AMAZON_ACCESS_ID'", \n\
        "secret": "'$AMAZON_ACCESS_KEY'", \n\
        "bucket": "'$AMAZON_BUCKET_NAME'", \n\
        "directory": "'$AMAZON_DIR_NAME'", \n\
        "region": "'$AMAZON_REGION'" \n\
    }, \n\
    "mode": "'$MODE'", \n\
    "bug_chat": '$BUG_CHAT' \n\
} \n\
' >> sets.json

# Run
CMD python app.py
