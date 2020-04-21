# Pull base image
FROM node:13.13.0

# Set work directory
WORKDIR .

# Install dependencies
COPY ./package.json .
RUN npm install

# # Set port
# EXPOSE 3000

# # Change settings & keys
# COPY ./docker/web/sets.js ./web/src/sets.js

# Copy project
COPY . .

# Create build
RUN npm run build

# # Run
# RUN npm install -g serve
# # CMD serve -s build -p 3000
# ENTRYPOINT ["bash", "run.sh"]