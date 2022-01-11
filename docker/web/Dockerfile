# Pull base image
FROM node:16.10 as web

# Set work directory
WORKDIR .

# Install dependencies
COPY ./package.json .
RUN npm install

# Copy project
COPY . .

# Settings
ARG PROTOCOL HOST
ENV SERVER "${PROTOCOL}://${HOST}/api/"
ENV CLIENT "${PROTOCOL}://${HOST}/"
ENV SOCKETS "${PROTOCOL}://${HOST}/"

# Run
RUN chmod +x /run.sh
CMD bash /run.sh
