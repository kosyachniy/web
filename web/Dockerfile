# Pull base image
FROM node:18.8

# Set work directory
WORKDIR .

# Install dependencies
COPY ./package.json .
RUN npm install

# Copy project
COPY . .

# Run
CMD npm run dev
