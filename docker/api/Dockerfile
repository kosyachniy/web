# Pull base image
FROM python:3.9.1

# Set work directory
WORKDIR .

# # Set environment variables
# ENV PYTHONDONTWRITEBYTECODE 1
# ENV PYTHONUNBUFFERED 1

# # Install system dependencies
# RUN apt update
# RUN pip install --upgrade pip

# Install dependencies
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# Copy project
COPY . .

# Settings
ARG SERVER
RUN echo "\n\nHOST=\"$SERVER\"" >> sets.py

# Run
CMD bash run.sh