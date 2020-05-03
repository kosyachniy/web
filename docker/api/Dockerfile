# Pull base image
FROM python:3.8.1-slim-buster

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

# # Set port
# EXPOSE 5000

# Copy project
COPY . .

# Settings
ARG SERVER
RUN if [ "x$SERVER" != "x" ] ; then echo "\n\nHOST=\"$SERVER\"" >> sets.py ; fi
RUN if [ "x$SERVER" = "x" ] ; then rm sets.py; cp sets.prod.py sets.py ; fi

# Run
ENTRYPOINT ["bash", "run.sh"]
# ENTRYPOINT ["gunicorn", "app:app", "-c", "run.py"]