FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt requirements.txt

RUN pip install --upgrade pip setuptools wheel
RUN pip install --prefer-binary -r requirements.txt

WORKDIR /app
COPY . /app
