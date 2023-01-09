# Pull base image
FROM node:19.3

# Set work directory
WORKDIR .

# Install dependencies
COPY ./package.json .
RUN npm i --production --force

# Copy project
COPY . .
