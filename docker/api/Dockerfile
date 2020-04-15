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
COPY /api/requirements.txt .
RUN pip install -r requirements.txt

# # Set port
# EXPOSE 5000

# Copy project
COPY . .

# Run
ENTRYPOINT ["bash", "entrypoint.sh"]
# ENTRYPOINT ["gunicorn", "app:app", "-c", "run.py"]