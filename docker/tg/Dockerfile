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
ARG PROTOCOL HOST TG_TOKEN MODE BUG_CHAT
RUN rm -f sets.json
RUN echo '{ \n\
    "server": "'$PROTOCOL'://'$HOST'/api/", \n\
    "tg": { \n\
        "server": "'$PROTOCOL'://'$HOST'/tg/", \n\
        "token": "'$TG_TOKEN'" \n\
    }, \n\
    "mode": "'$MODE'", \n\
    "bug_chat": '$BUG_CHAT' \n\
} \n\
' >> sets.json

# Run
CMD python app.py
