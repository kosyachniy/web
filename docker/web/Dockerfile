# Pull base image
FROM node:13.13.0 as web

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

# Settings
ARG SERVER
RUN if [ "x$SERVER" = "x" ] ; then rm src/sets.js; cp src/sets.prod.js src/sets.js ; fi

# Create build
RUN npm run build
RUN ls /build

# # Run
# RUN npm install -g serve
# # # CMD serve -s build -p 3000
# ENTRYPOINT ["bash", "run.sh"]

# NGINX
FROM nginx
COPY --from=web /build /web/build