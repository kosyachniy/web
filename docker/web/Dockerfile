# Pull base image
FROM node:13.13.0

# # Install chrome for protractor tests
# RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
# RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list'
# RUN apt-get update && apt-get install -yq google-chrome-stable

# Set work directory
WORKDIR .

# # add `/app/node_modules/.bin` to $PATH
# ENV PATH /app/node_modules/.bin:$PATH

# Install dependencies
COPY ./package.json .
RUN npm install
RUN echo 'hello world'

# # Set port
# EXPOSE 3000

# Copy project
COPY . .

# Run
# CMD ng serve --host 0.0.0.0 --port 4200
ENTRYPOINT ["npm", "start"]