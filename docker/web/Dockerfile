# Pull base image
FROM node:15.5.1 as web

# Set work directory
WORKDIR .

# Install dependencies
COPY ./package.json .
RUN npm install

# Copy project
COPY . .

# Run
CMD npm start