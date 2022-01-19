# Pull base image
FROM python:3.9.10

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
ARG PROTOCOL HOST
ENV SERVER "${PROTOCOL}://${HOST}/api/"
ENV CLIENT "${PROTOCOL}://${HOST}/"
ENV MONGO_HOST "db"
