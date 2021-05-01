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
ARG HOST PORT SIDE_OPTIMIZED MONGO_LOGIN MONGO_PASSWORD GOOGLE_ID GOOGLE_SECRET TG_TOKEN SMSC_LOGIN SMSC_PASSWORD VK_ID VK_SECRET
RUN rm -f sets.json keys.json
RUN echo "{\"mongo\": {\"host\": \"db\", \"db\": \"uple\"}, \"client\": \"$HOST:$PORT/\", \"side_optimized\": $SIDE_OPTIMIZED}" >> sets.json
RUN echo "{\"mongo\": {\"login\": \"$MONGO_LOGIN\", \"password\": \"$MONGO_PASSWORD\"}, \"google\": {\"client_id\": \"$GOOGLE_ID\", \"client_secret\": \"$GOOGLE_SECRET\"}, \"tg\": {\"token\": \"$TG_TOKEN\"}, \"smsc\": {\"login\": \"$SMSC_LOGIN\", \"password\": \"$SMSC_PASSWORD\"}, \"vk\": {\"client_id\": $VK_ID, \"client_secret\": \"$VK_SECRET\"}}" >> keys.json

# Run
CMD bash run.sh