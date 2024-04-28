FROM node:19.8

COPY package.json package.json
RUN npm i --production --force

WORKDIR /app
COPY . /app
