# Pull base image
FROM python:3.10

# Set work directory
WORKDIR /app

# Copy project
COPY . /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
# NOTE: Using Russian text may lead to errors 0, 137
# Output print to the Docker console
ENV PYTHONUNBUFFERED 1

# Install dependencies
RUN pip install -r requirements.txt
